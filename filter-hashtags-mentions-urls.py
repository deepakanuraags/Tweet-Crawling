import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time
import re
import emoji
import fnmatch
from datetime import datetime
import pytz
from datetime import datetime



class FilterHashTagsMentionsURLS:

    def filterHashTags(self,lang,user):
            currentCount  = 100
            filewithEmoticons = ''
            
            userTweetJsonFiles = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user) if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + f)]
            usetTweetJsonReplyTweets = []
            userTweetHashTagTweets = []
            userTweetJsonFiles = [f for f in userTweetJsonFiles if fnmatch.fnmatch(os.getcwd() + '/' + lang + '/' + user + '/' + f, '*.json')]
            print(userTweetJsonFiles)
            print(usetTweetJsonReplyTweets)
            print(userTweetHashTagTweets)
            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/replyTweets'):
              usetTweetJsonReplyTweets = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user + '/replyTweets') if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'+ '/' + f) and 
               fnmatch.fnmatch(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'+ '/' + f, '*.json')]

            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/hashTags'):
              userTweetHashTagTweets = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user + '/hashTags') if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + 'hashTags'+ '/' + f)
               and fnmatch.fnmatch(os.getcwd() + '/' + lang + '/' + user + '/' + 'hashTags'+ '/' + f, '*.json')]  
            
            for tweetFileName in userTweetJsonFiles:
              tweets = []
              path = os.getcwd()+ '/'+ lang + '/' +  user   + '/' + tweetFileName
              print(path)
              with open(path) as json_file:
               tweets = json.load(json_file)

              tweets = self.fetchSeperateFields(tweets,tweetFileName)

              with open(path,'w') as json_file:
                  json.dump(tweets,json_file,ensure_ascii=False)

            for tweetFileName in usetTweetJsonReplyTweets:
              tweets = []
              path = os.getcwd()+ '/'+ lang + '/' +  user   + '/replyTweets/' + tweetFileName
              print(path)
              with open(path) as json_file:
               tweets = json.load(json_file)

              tweets = self.fetchSeperateFields(tweets,tweetFileName)

              with open(path,'w') as json_file:
                  json.dump(tweets,json_file,ensure_ascii=False)

            print('file with emoticons')
            print(filewithEmoticons)
            # for tweetFileName in userTweetHashTagTweets:
            #   tweets = []
            #   path = os.getcwd()+ '/'+ lang + '/' +  user   + '/hashTags/' + tweetFileName
            #   print(path)
            #   with open(path) as json_file:
            #    tweets = json.load(json_file)

            #   tweets = self.fetchSeperateFields(tweets)

            #   with open(path,'w') as json_file:
            #       json.dump(tweets,json_file,ensure_ascii=False)



            # if os.path.exists(os.getcwd() + '/' + lang + '/' + user):

            #  for 

            # if specificFile is None 
            
            # while shouldBreak == False:

            #   if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+ user  + '_tweets_' + str(currentCount + 100) + '.json'):
            #       print(os.getcwd()+ '/'+  lang +'/' + user + '/'+ user  + '_tweets_' + str(currentCount + 100))
            #       shouldBreak = True
            #   else :
            #       currentCount = currentCount + 100
            #       print('in else ' + str(currentCount))


            # with open(os.getcwd()+ '/'+ lang + '/' +  user   +"/replyTweets/realDonaldTrump_reply_tweets_1168326060280307712_25.json") as json_file:
            #   tweets = json.load(json_file)





    def fetchSeperateFields(self,tweets,tweetFileName):
            for tweet in tweets:
                # hashTags = re.findall(r"#(\w+)", tweet['text'])
                # print(tweet['text'])
                # print(hashTags)
          
                hashTagsFiltered = self.hashtags123(tweet)
                hashTagModified = []
                for hashTG in hashTagsFiltered:  
                  hashTG = re.sub('[#]', '', hashTG)
                  hashTagModified.append(hashTG)
                
                print(tweet['text'])
                
                print('hashtags')
                print(hashTagModified)
                tweet['hashtags'] = hashTagModified
                
                mentionsFiltered = self.filterMentions(tweet)
                print('mentions')
                print(mentionsFiltered)
                tweet['mentions'] = mentionsFiltered

                URLSFiltered = self.filterURLs(tweet)
                print('Urls')
                print(URLSFiltered)
                tweet['tweet_urls'] = URLSFiltered

                emojis_filtered = self.extract_emojis(tweet)
                if len(emojis_filtered)>0:
                    self.filewithEmoticons = tweetFileName
                print('emoji filterd')
                print(emojis_filtered)
                tweet['tweet_emoticons'] = emojis_filtered
                print("******************************************")

                tweet['tweet_date'] =  self.getFormattedDate(tweet)

                self.modifyPOIname_POIid_replyText_tweetText(tweet)
            return tweets


    def hashtags123(self,tweet):
        return list(filter(lambda token: token.startswith('#'), tweet['text'].split()))

    def filterMentions(self, tweet):
        text = re.sub("[\w]+@[\w]+\.[c][o][m]", "", tweet['text'])
        result = re.findall("@([a-zA-Z0-9]{1,15})", text)
        return result

    def filterURLs(self,tweet):
        result = re.findall(r'(https?://[^\s]+)', tweet['text'])
        return result

    def extract_emojis(self,tweet):
        return [c for c in tweet['text'] if c in emoji.UNICODE_EMOJI]
    
    def getFormattedDate(self,tweet):
        print(tweet['created_at'])
        dataObj = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y')
        dataObj = dataObj.replace(minute = 0,second = 0)
        print(dataObj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        return dataObj.strftime("%Y-%m-%dT%H:%M:%SZ")

    def modifyPOIname_POIid_replyText_tweetText(self,tweet):
        print(tweet['text'])
        tweet['tweet_text'] = tweet['text']
        tweet['tweet_lang'] = tweet['lang']
        if not tweet['in_reply_to_status_id'] is None:
            tweet['reply_text'] = tweet['text']
            tweet['replied_to_tweet_id'] = tweet['in_reply_to_status_id']
            tweet['replied_to_user_id'] = tweet['in_reply_to_user_id']
            tweet['poi_id'] = tweet['in_reply_to_user_id']
            tweet['poi_name'] = tweet['in_reply_to_screen_name']
        else:
            tweet['tweet_text'] = tweet['text']
            tweet['reply_text'] = None
            tweet['replied_to_tweet_id'] = None
            tweet['replied_to_user_id'] = None
            tweet['poi_id'] = tweet['user']['id']
            tweet['poi_name'] = tweet['user']['screen_name']
        

if __name__ == '__main__':
      
       filterArtifacts = FilterHashTagsMentionsURLS()
       filterArtifacts.filterHashTags('pt','MarceloFreixo')

 