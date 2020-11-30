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


class loadReplyTweets():

     def loadRepliesForPOITweets(self,sourceId,maxId,user,langOfTweets,country):
       totalRepliesForCurrentTweet = 0
       loopCount = 0
       totalRepliesForCurrentTweet = []
       while len(totalRepliesForCurrentTweet) < 25 :
                 loopCount = loopCount + 1
                #  if (loopCount == 3 and len(totalRepliesForCurrentTweet) ==0):
                #     break
                #  reply_tweets =[]
                 reply_tweets = self.crawlReplyTweetsForUserAndSinceId(user,langOfTweets,200,sourceId,maxId)
                 if len(reply_tweets) > 0 :
                   if loopCount>3 and len(totalRepliesForCurrentTweet)==0 or loopCount>6 and len(totalRepliesForCurrentTweet)<10: 
                      print('breaking the loop')
                      break
                   filtered_reply_tweets = self.processReplyTweets(sourceId,reply_tweets,langOfTweets) 
                   totalRepliesForCurrentTweet = totalRepliesForCurrentTweet + filtered_reply_tweets
                   maxId = reply_tweets[len(reply_tweets) - 1].id - 1
                  
                   print("current replies count")
                   print(len(totalRepliesForCurrentTweet))
                   print("*********************** \n ************************")

                 else:
                   break 
                
       if(len(totalRepliesForCurrentTweet)>=25):
         if not os.path.exists(os.getcwd()+ '/'+ user  + '/replyTweets'):
          print("directory not existing creating one")
          os.mkdir(os.getcwd()+ '/'+ user  + '/replyTweets')

         print("writing into file") 
         replyfilepath = os.getcwd()+ '/'+ user  + '/replyTweets/' + user + '_reply_tweets_'+ str(sourceId) + '_' + str(len(totalRepliesForCurrentTweet)) + '.json'
         print(replyfilepath)

         modifiedTweets = []
         for tweet in totalRepliesForCurrentTweet:
         
            tweet._json['country'] = country 
            modifiedTweets.append(tweet._json)

         with open(replyfilepath,'a') as fou:  
           json.dump(modifiedTweets,fou)

         print('successful')
         return 'successful'

       else:
         print('unsuccessful')
         return 'unsuccessful' 

     def crawlReplyTweetsForUserAndSinceId(self,user,langOfTweets,repliesCount,sinceId,maxId):
         query = 'to:' + user
         print(query)
         if maxId > 0:
           reply_tweets = api.search(q = query ,lang=langOfTweets,count = repliesCount , result_type='recent' , since_id=sinceId, max_id = maxId)
           print("fetched with max id")
           print(len(reply_tweets))
           print("max id")
           print(maxId)
         else:
           reply_tweets = api.search(q = query ,lang=langOfTweets,count = repliesCount , result_type='recent' , since_id=sinceId)
           print("fetched without max id")
           print(len(reply_tweets))

         return reply_tweets

     def processReplyTweets(self,sourceTweetId,replyTweets,langOfTweets):
         filteredReplyTweets = []
         for tweet in replyTweets:
             if hasattr(tweet, 'in_reply_to_status_id_str'):
                #  print("replyTweet: ")
                #  print(tweet.in_reply_to_status_id_str)
                #  print("sourceTweet: ")
                #  print(sourceTweet.id_str)
                 if (tweet.in_reply_to_status_id_str==str(sourceTweetId)):
                    print("found one tweet")
                    filteredReplyTweets.append(tweet)
        
        #  filteredReplyTweets = [tweet for tweet in filteredReplyTweets if tweet.lang == langOfTweets]
         filteredReplyTweets = [tweet for tweet in filteredReplyTweets if not hasattr(tweet, 'retweeted_status')] 
         print("processed reply tweets")
         print(len(filteredReplyTweets))
         return filteredReplyTweets


class readTweetIdsOfPOIs():
       def getInBetweenTweetIds(self,user,topMostId,bottomMostId):
         tweets = []
         filteredTweetIds = []
         with open(os.getcwd()+ '/'+ user  + '/' + user + '_tweets_100.json') as json_file:
          tweets = json.load(json_file)
          
         for tweet in tweets:
          #  print(tweet)
          #  print('/n')
           if tweet['id'] <= topMostId and tweet['id'] >= bottomMostId :
              filteredTweetIds.append(tweet['id'])
         print(filteredTweetIds)
         return filteredTweetIds

       def recursivelyFetchReplies(self,tweetIdsReplysToFetch,user,languageOfTweets,locationOfTweets,outerBoundaryOfTopTweetId):
              for idx,tweetId in enumerate(tweetIdsReplysToFetch):
                print('fetching for tweet id')
                print(tweetId)
                crawlTweets = loadReplyTweets()
                status = 'unsuccessful'

                if idx == 0:
                  sinceId = tweetId
                  maxId = outerBoundaryOfTopTweetId
                  while status != 'successful':
                    status = crawlTweets.loadRepliesForPOITweets(sinceId,maxId,user,languageOfTweets,locationOfTweets)
                    maxId = 0
                    if status == 'successful':
                      break
                else :
                  sinceId = tweetId
                  # maxId = tweetIdsReplysToFetch[idx-1]
                  currentNumberToMinus = 0
                  while status != 'successful':
                    currentNumberToMinus = currentNumberToMinus+1
                    print(tweetIdsReplysToFetch)
                    print(currentNumberToMinus)
                    print(idx - currentNumberToMinus)

                    if (idx - currentNumberToMinus >=0): 
                      maxId = tweetIdsReplysToFetch[idx-currentNumberToMinus]
                    elif maxId != outerBoundaryOfTopTweetId:
                      maxId = outerBoundaryOfTopTweetId
                    else :
                      maxId = 0  

                    status = crawlTweets.loadRepliesForPOITweets(sinceId,maxId,user,languageOfTweets,locationOfTweets)

                    if status == 'successful':
                      break

                print('successful')


         

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    # l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,  wait_on_rate_limit=True)
    outerBoundaryOfTopTweetId = 1169375550806351872
    readTweetIds = readTweetIdsOfPOIs()
    tweetIdsReplysToFetch = readTweetIds.getInBetweenTweetIds('realDonaldTrump',1169253298169438208,1169062380040523776)
    readTweetIds.recursivelyFetchReplies(tweetIdsReplysToFetch,'realDonaldTrump','en','USA',outerBoundaryOfTopTweetId)

    # crawlTweets = loadReplyTweets()
    # crawlTweets.loadRepliesForPOITweets(1169253299981303810,1169356701943894017,'realDonaldTrump','en','USA')