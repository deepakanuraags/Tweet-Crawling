import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time

access_token = '1166721367619899392-pHVNKXpkrNrs2iWwaE7fc9ifvURboP'
access_token_secret = 'IuQfuEiZG3hDj8hWmtsq9OLnQhWosTTsNi4VGwn14zfsx'
consumer_key = 'vQjLuPJ1wvmLhiJZrS2bvSTdC'
consumer_secret = 'SpKUPIbajh67ytpqb1YqT7I0Kqb7QI4TGBFRElOtTOKCwnY1TV'


class loadReplies:
    
    def loadRepliesInTimePeriod(self,sinceId,maxId,user,lang,country):
        reply_tweets = []
        totalRepliesForCurrentTweet = []
        count = 0
        existing_tweets = []
        while len(reply_tweets) != 0 or count == 0 :
            count = count +1
            print('current max id')
            print(maxId)   
            query = 'to:' + user
            print(query)
            reply_tweets = api.search(q = query , result_type='recent' ,count = 200, since_id=sinceId, max_id = maxId)
            print('number of loaded tweets' + str(len(reply_tweets)))
            filtered_reply_tweets = [tweet for tweet in reply_tweets if not hasattr(tweet, 'retweeted_status')] 
            print('number of loaded tweets with retweets removed' + str(len(filtered_reply_tweets)))
            totalRepliesForCurrentTweet = totalRepliesForCurrentTweet + filtered_reply_tweets
            if len(reply_tweets) != 0 : 
             maxId = reply_tweets[len(reply_tweets) - 1].id - 1
            modifiedTweets = []
            for tweet in filtered_reply_tweets:
                tweet._json['country'] = country 
                modifiedTweets.append(tweet._json)

            if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user  + '/utils'):
             print("directory not existing creating one")
             os.mkdir(os.getcwd()+ '/' + lang + '/' + user  + '/utils')

            if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user  + '/utils/'+ user + '_replies.json'):
             print("file not existing creating one")
             with open(os.getcwd()+ '/'+ lang +'/'+ user  + '/utils/' + user + '_replies.json','a') as json_file:
                  tweets_temp = []
                  json.dump(tweets_temp,json_file)
          
            # with open(os.getcwd()+ '/'+ lang +'/'+ user  + '/utils/' + user + '_replies.json') as json_file:
            # existing_tweets = json.load(json_file)
             
             existing_tweets = existing_tweets + modifiedTweets
            # #  json.dump(existing_tweets,json_file)

            # with open(os.getcwd()+ '/'+ lang +'/'+ user  + '/utils/' + user + '_replies.json','w') as json_file:
            #  json.dump(existing_tweets,json_file)
        
        with open(os.getcwd()+ '/'+ lang +'/'+ user  + '/utils/' + user + '_replies.json','w') as json_file:
             json.dump(existing_tweets,json_file)




        

            




if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    # l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,  wait_on_rate_limit=True,wait_on_rate_limit_notify = True)
    # outerBoundaryOfTopTweetId = 1169375550806351872
    # readTweetIds = readTweetIdsOfPOIs()
    # tweetIdsReplysToFetch = readTweetIds.getInBetweenTweetIds('realDonaldTrump',1169253298169438208,1169062380040523776)
    # readTweetIds.recursivelyFetchReplies(tweetIdsReplysToFetch,'realDonaldTrump','en','USA',outerBoundaryOfTopTweetId)

    loadReplyTweets = loadReplies()
    loadReplyTweets.loadRepliesInTimePeriod(1168464414779105285,1170828700960661510,'jairbolsonaro','pt','Brazil')