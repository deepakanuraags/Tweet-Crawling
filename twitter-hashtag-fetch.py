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


class FetchHashTags:

    def fetchHashTags(self,query,user,langOfTweets,filtername):
         query = '# ' + user
         totalTweetsWithhashTags = []
         maxId = 0 
         total_hashtag_tweets = []
         while len(totalTweetsWithhashTags) < 2000 :
            #  loopCount = loopCount + 1
             if maxId == 0 :  
                hashTagTweets = api.search(q = query ,count = 2000 , result_type='recent')
             else :
                hashTagTweets = api.search(q = query ,count = 2000 , result_type='recent',max_id = maxId)
                    
             print('hashfetch : ' + str(len(hashTagTweets)))
             if len(hashTagTweets) > 0 :
                 maxId = hashTagTweets[len(hashTagTweets) - 1].id - 1
                 filtered_hashtag_tweets = self.processTweets(hashTagTweets,filtername) 
                 print('filter : '+ str(len(filtered_hashtag_tweets)))
                 totalTweetsWithhashTags = totalTweetsWithhashTags + filtered_hashtag_tweets
                 print('total tweets: ' + str(len(totalTweetsWithhashTags)))

                   
             else:
                 break 

             if not os.path.exists(os.getcwd()+ '/'+  langOfTweets +'/' + user  + '/hashTags'):
                 print("directory not existing creating one")
                 os.mkdir(os.getcwd() + '/'  + langOfTweets + '/'+ user  + '/hashTags')
                  
                 print("current replies count")
                 print(len(totalTweetsWithhashTags))
                 print("*********************** \n ************************")

         tempTweetArray = []
         currentTweetBatch = 100
         for idx,tweet in enumerate(totalTweetsWithhashTags):
                #  print('inside for loop')
                 tempTweetArray.append(tweet._json)
                 if idx % 100 == 0 and idx>=100:
                   temp2TweetArray = tempTweetArray
                   tempTweetArray = []
                   with open(os.getcwd()+ '/'+  langOfTweets +   '/' + user  + '/' + 'hashTags/' + user + '_hash_' + str(currentTweetBatch)+ '.json','w') as fou:
                     json.dump(temp2TweetArray,fou)
                   currentTweetBatch = currentTweetBatch + 100
                   tempTweetArray = []
             
                 if idx == (len(totalTweetsWithhashTags) - 1):
                     with open(os.getcwd()+ '/'+   langOfTweets +   '/' + user  + '/' + 'hashTags/'  + user + '_hash_' + str(currentTweetBatch)+ '.json','w') as fou:
                          json.dump(tempTweetArray,fou)

    def processTweets(self,tweets,filtername):
        #  for tweet in tweets:
        #     print(tweet.text.find('@realDonaldTrump'))
         filteredTweets = [tweet for tweet in tweets if not hasattr(tweet, 'retweeted_status')]
        #  filteredTweets = [tweet for tweet in filteredTweets if tweet.text.find('#ewarren') > -1 or tweet.text.find(filtername) > -1]
         filteredTweets = [tweet for tweet in filteredTweets if tweet.text.find('@ewarren') == -1] 
         return filteredTweets 

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    # l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify = True)
    crawlTweets = FetchHashTags()
    crawlTweets.fetchHashTags('(#speakerPelosi OR #pelosi)','SpeakerPelosi','en','Nancy Pelosi')