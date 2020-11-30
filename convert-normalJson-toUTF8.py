import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time


class convertToUTF8:
     def convertJsonToUTF(self,lang,user):
            
            userTweetJsonFiles = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user) if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + f)]
            usetTweetJsonReplyTweets = []
            userTweetHashTagTweets = []

            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/replyTweets'):
              usetTweetJsonReplyTweets = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user + '/replyTweets') if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'+ '/' + f)]

            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/hashTags'):
              userTweetHashTagTweets = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user + '/hashTags') if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + 'hashTags'+ '/' + f)]  
            
            print(str(len(userTweetJsonFiles)))
            print(str(len(usetTweetJsonReplyTweets)))

            for file in userTweetJsonFiles:
                
              with open(os.getcwd() + '/' + lang + '/' + user + '/' + file) as json_file:
                fileLoaded = False
                
                try:
                   with open(os.getcwd() + '/' + lang + '/' + user +'/'   + file) as json_file:
                      fileLoaded = True 
                      tweetFile = json.load(json_file)
                except:
                  print("this tweets file was not converted into utf ")
                  print(os.getcwd() + '/' + lang + '/' + user + '/'   + file) 


              if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF'):
                 os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF')

              if fileLoaded == True:   
                   with open(os.getcwd() + '/' + lang + '/' + user + '/' +  'UTF'+'/' +file,'w') as fou:  
                      json.dump(tweetFile,fou,ensure_ascii=False)

            for file in usetTweetJsonReplyTweets: 
                fileLoaded = False
                
                try:
                 with open(os.getcwd() + '/' + lang + '/' + user + '/replyTweets/'   + file) as json_file:
                  tweetFile = json.load(json_file)
                  fileLoaded = True
                except:
                  print("this reply file was not converted into utf ")
                  print(os.getcwd() + '/' + lang + '/' + user + '/replyTweets/'   + file)


                if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF'):
                  os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF')

                if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF' + '/' + 'replyTweets'):
                  os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF' + '/' + 'replyTweets')
                
                if fileLoaded == True:
                    with open(os.getcwd() + '/' + lang + '/' + user + '/' +  'UTF'+'/' + 'replyTweets' + '/' + file ,'w') as fou:  
                       json.dump(tweetFile,fou,ensure_ascii=False)

            for file in userTweetHashTagTweets: 
                with open(os.getcwd() + '/' + lang + '/' + user + '/hashTags/'   + file) as json_file:
                  tweetFile = json.load(json_file)


                if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF'):
                  os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF')
                
                if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF' + '/' + 'hashTags'):
                  os.mkdir(os.getcwd()+ '/'+  lang +'/' + user + '/'+  'UTF' + '/' + 'hashTags')
                 
                with open(os.getcwd() + '/' + lang + '/' + user + '/' +  'UTF'+'/' + 'hashTags' + '/' + file ,'w') as fou:  
                   json.dump(tweetFile,fou,ensure_ascii=False)


            for file in userTweetHashTagTweets:
               
               if not os.path.exists(path +  '/' + lang +  '/' + user + '/updatedHashTags'):
                print("directory not existing creating one")
                os.mkdir(path + '/' + langOfTweets + '/' + user)
               with open(os.getcwd() + '/' + lang + '/' + user + '/hashTags/'   + file) as json_file:
                  tweetFile = json.load(json_file)
               tweets = []
               tweets = [tweet for tweet in tweetFile if tweet.in_reply_to_status_id is None] 

               with open(os.getcwd() + '/' + lang + '/' + user + '/' +  'UTF'+'/' + 'hashTags' + '/' + file ,'w') as fou:  
                   json.dump(tweetFile,fou,ensure_ascii=False)


if __name__ == '__main__':           
    
    convertToUTF8 = convertToUTF8()
    convertToUTF8.convertJsonToUTF('pt','MarceloFreixo')