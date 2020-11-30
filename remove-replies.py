import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time


class filterReplyTweets():

    def filterReplyTweets1(self,lang,user,fileName):
        # userTweetJsonFiles = [f for f in os.listdir(os.getcwd() + '/' + lang + '/' + user) if os.path.isfile(os.getcwd() + '/' + lang + '/' + user + '/' + f)]

        # for tweetFileName in userTweetJsonFiles:
              tweets = []
              path = os.getcwd()+ '/'+ lang + '/' +  user   + '/' + fileName
              print(path)
              with open(path) as json_file:
               tweets = json.load(json_file)

              filteredTweets = [tweet for tweet in tweets if tweet['in_reply_to_status_id'] is None] 

              with open(os.getcwd()+ '/'+ lang + '/' +  user   + '/' + 'tweets_updated_'+ str(len(filteredTweets)) + '.json','w') as json_file:
                  json.dump(filteredTweets,json_file,ensure_ascii=False)





if __name__ == '__main__':

    Abc = filterReplyTweets()
    Abc.filterReplyTweets1('hi','yadavakhilesh','tweets_1060.json')

              

