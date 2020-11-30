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

class ReadTweetsFromJson:
    def readTweetsFromJsonWithIds(self,topMostId,bottomMostId,user,lang):
        filteredTweetIds = []
        loadedTweetsOfPOIs = []
        replyTweets = []
        
        with open(os.getcwd()+ '/'  + lang +   '/'+ user  + '/' +  user + '_tweets_100.json') as json_file:
          loadedTweetsOfPOIs = json.load(json_file)
          
        for tweet in loadedTweetsOfPOIs:
            if tweet['id'] <= topMostId and tweet['id'] >= bottomMostId :
              filteredTweetIds.append(tweet['id'])

        with open(os.getcwd()+ '/'  + lang + '/'+ user  + '/utils' + '/' + user + '_replies.json') as json_file:
             replyTweets = json.load(json_file)

        for tweetId in filteredTweetIds:
             matchingReplyTweets = []
             matchingReplyTweets = [replytweet for replytweet in replyTweets if replytweet['in_reply_to_status_id'] == tweetId] 
             
             if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user  + '/replyTweets'):
              print("directory not existing creating one")
              os.mkdir(os.getcwd() + '/'  + lang + '/'+ user  + '/replyTweets')

             with open(os.getcwd()+ '/'+ lang +'/'+ user  + '/replyTweets/' + user + '_reply_tweets_' + str(tweetId) + '_' + str(len(matchingReplyTweets)) +'.json','w') as json_file:
              print('writing replies for ' + str(tweetId))
              json.dump(matchingReplyTweets,json_file)






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

    loadReplyTweets = ReadTweetsFromJson()
    loadReplyTweets.readTweetsFromJsonWithIds(1168464414779105285,1170108705242853379,'jairbolsonaro','pt')