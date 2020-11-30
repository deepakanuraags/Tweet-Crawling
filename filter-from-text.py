import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time
import re,string
import re
import fnmatch

class FilterFromTweetText:
        
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        

        def filterTweets(self,lang,user):

            userTweetJsonFiles = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user) if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + f)]
            usetTweetJsonReplyTweets = []
            userTweetHashTagTweets = []
            userTweetJsonFiles = [f for f in userTweetJsonFiles if fnmatch.fnmatch(os.getcwd() + '/' + lang + '/' + user + '/' + f, '*.json')]
            # print(userTweetJsonFiles)
            # print(usetTweetJsonReplyTweets)
            # print(userTweetHashTagTweets)
            # time.sleep(10)
            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/replyTweets'):
              usetTweetJsonReplyTweets = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user + '/replyTweets') if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'+ '/' + f) and 
               fnmatch.fnmatch(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'+ '/' + f, '*.json')]
              
            finalTweets = []
            for idx,tweetFileName in enumerate(userTweetJsonFiles):
                #   print(idx)
                #   print(tweetFileName)
                #   time.sleep(5)
                  tweets = []
                  path = os.getcwd()+ '/'+ lang + '/' +  user   + '/' + tweetFileName
                #   print(path)
                  with open(path) as json_file:
                     tweets = json.load(json_file)
                  
                  tweets = self.testLogic(tweets,lang)
                  finalTweets = finalTweets + tweets

            finalReplies = []
            for tweetFileName in usetTweetJsonReplyTweets:
                  tweets = []
                  path = os.getcwd()+ '/'+ lang + '/' +  user   + '/replyTweets/' + tweetFileName
                #   print(path)
                  with open(path) as json_file:
                      tweets = json.load(json_file)
                  
                  tweets = self.testLogic(tweets,lang)
                  finalReplies = finalReplies + tweets

            if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'Final'):
                 os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'Final')

            with open(os.getcwd()+ '/'+ lang + '/' +  user   + '/' + 'Final/' + 'tweets_' + str(len(finalTweets)) +'.json','w') as json_file:
                  json.dump(finalTweets,json_file,ensure_ascii=False)

            if len(finalReplies) > 0 :
                 with open(os.getcwd()+ '/'+ lang + '/' +  user   + '/' + 'Final/' + 'replies_' + str(len(finalReplies)) + '.json','w') as json_file:
                      json.dump(finalReplies,json_file,ensure_ascii=False)
                      

                

        
        def strip_links(self,text):

             link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
             links         = re.findall(link_regex, text)
             for link in links:
               text = text.replace(link[0], ', ')    
             return text

        def strip_all_entities(self,text):

             entity_prefixes = ['@','#']
             for separator in  string.punctuation:
               if separator not in entity_prefixes :
                  text = text.replace(separator,' ')
             words = []
             for word in text.split():
                 word = word.strip()
                 if word:
                   if word[0] not in entity_prefixes:
                       words.append(word)
             return ' '.join(words)
            
        def testLogic(self,tweets,lang):
            
            tests = [
                 "@peter I really love that shirt at #Macy. http://bet.ly//WjdiW4",
                 "@shawn Titanic tragedy could have been prevented Economic Times: Telegraph.co.ukTitanic tragedy could have been preve... http://bet.ly/tuN2wx",
                 "I am at Starbucks http://4sh.com/samqUI (7419 3rd ave, at 75th, Brooklyn)",
                 "I tawt I taww ah puttycat😼 #123123 ,.,./;'#123123"
                ]

            filteredTweets = []
            for t in tweets:
                #   print(t['text'])
                  value =  self.strip_all_entities(self.strip_links(t['text']))
                  value =  self.strip_emoji(value)
                  value =  self.strip_punctuations(value)
                  if t['lang'] == 'und':
                      t['lang'] = lang
                      print(t['lang'])
                  field = 'text_' + t['lang']
                  t[field] = value
                #   print(t[field])
            
            return tweets

        def strip_emoji(self,text):
             return self.RE_EMOJI.sub(r'', text)

        def strip_punctuations(self,text):
             return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())




if __name__ == '__main__':
      
       filterTweetText = FilterFromTweetText()
       filterTweetText.filterTweets('pt','MarceloFreixo')
        
