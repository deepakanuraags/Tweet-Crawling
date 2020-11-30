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


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


class TweepyCrawlTweets():
     max_id = 0
     def crawlForThisUser(self,user,tweetcount,langOfTweets,locationOfTweets):
        #  user_tweets = [status._json for status in tweepy.Cursor(api.user_timeline,  screen_name = user , count = tweetcount , result_type='recent')]
         print("step 1")
         crawledCount = 0
         finalTweets = []
         user_tweets = self.fetchTweets(user,tweetcount)
         filtered_tweets = self.processTweets(user_tweets,langOfTweets)
         finalTweets = finalTweets + filtered_tweets
         finalReplyTweets = []
         crawledCount = len(finalTweets)
         print("current final Tweet Count")
         print(len(finalTweets))
         
         loopCount = 0
         totalUserTweets = []
         totalUserTweets = totalUserTweets + user_tweets
         while len(totalUserTweets) < tweetcount:
            loopCount = loopCount + 1
            print("loop count")
            print(loopCount)
        #    if len(user_tweets) > 0 :
            print("total user tweets")
            print(len(totalUserTweets))
            user_tweets = self.fetchTweetsMaxId(user,tweetcount,self.max_id)
            totalUserTweets = totalUserTweets + user_tweets
            filtered_tweets = self.processTweets(user_tweets,langOfTweets)
            finalTweets = finalTweets + filtered_tweets
            crawledCount = len(finalTweets)
            
            print("if current final Tweet Count")
            print(len(finalTweets))
           
        #    else:
        #     finalTweets = finalTweets + user_tweets
        #     crawledCount = crawledCount + len(user_tweets)
        #     print("else current crawled count")
        #     print(crawledCount)
        #     print("else current final Tweet Count")
        #     print(len(finalTweets))
        #     break

        # #  finalTweets = [tweet for tweet in finalTweets if tweet.id == 1169815874988986369] 
        #  totalRepliesForThisUser = 0
        #  for tweet in finalTweets:
        #      print("entered replies area")
        #      totalRepliesForCurrentTweet = []
        #      sinceId = tweet.id
        #      maxId = 0
        #      loopCount = 0 
        #      while len(totalRepliesForCurrentTweet) < 100 :
        #          loopCount = loopCount + 1
        #         #  if (loopCount == 3 and len(totalRepliesForCurrentTweet) ==0):
        #         #     break
        #         #  reply_tweets =[]
        #          reply_tweets = self.crawlReplyTweetsForUserAndSinceId(user,langOfTweets,200,sinceId,maxId)
        #          if len(reply_tweets) > 0:
        #         #   sinceId = reply_tweets[len(reply_tweets)-1].id
        #           filtered_reply_tweets = self.processReplyTweets(tweet,reply_tweets,langOfTweets) 
        #           totalRepliesForCurrentTweet = totalRepliesForCurrentTweet + filtered_reply_tweets
        #           maxId = reply_tweets[len(reply_tweets) - 1].id - 1
                  
        #           print("current replies count")
        #           print(len(totalRepliesForCurrentTweet))
        #           print("*********************** \n ************************")

        #          else:
        #           break 
            
        #      if len(totalRepliesForCurrentTweet) > 20 : 
        #        print("good tweet")


        #      totalRepliesForThisUser = totalRepliesForThisUser + len(totalRepliesForCurrentTweet)
        #      print("totalRepliesForThisUser")
        #      print(totalRepliesForThisUser)

            #  finalReplyTweets = finalReplyTweets + totalRepliesForCurrentTweet

         print("the current directory is")
         print(os.getcwd())
         path = os.getcwd()

         if not os.path.exists(path +  '/' + langOfTweets +  '/' + user):
            print("directory not existing creating one")
            os.mkdir(path + '/' + langOfTweets + '/' + user)
            
         filepath = os.getcwd()+ '/'+  langOfTweets +   '/'  + user  + '/' + user + '_tweets.json'
         print(filepath)

         replyfilepath = os.getcwd()+ '/'+ user  + '/' + user + 'reply_tweets1.json'
         print(replyfilepath)
           
         if os.path.exists(filepath):
            print("removing" + filepath)
            os.remove(filepath)
        
         if os.path.exists(replyfilepath):
            print("removing" + replyfilepath)
            os.remove(replyfilepath)

         currentTweetBatch = 100
         tempTweetArray = []
         for idx,tweet in enumerate(finalTweets):
        #    print('opening json file')
           
           tweet._json['country'] = locationOfTweets
        #    print("country")
        #    print(tweet._json)
        #    print("location of tweets")
        #    print(locationOfTweets)
        #    print(tweet)

        #    jsonTweet = tweet._json
        #    jsonTweet.country = locationOfTweets
           tempTweetArray.append(tweet._json)
           if idx % 100 == 0 and idx>=100:
             temp2TweetArray = tempTweetArray
             tempTweetArray = []
             with open(path+ '/'+  langOfTweets +   '/' + user  + '/' + user + '_tweets_' + str(currentTweetBatch)+ '.json','w') as fou:
              json.dump(temp2TweetArray,fou)
             currentTweetBatch = currentTweetBatch + 100
             tempTweetArray = []
             
           if idx == (len(finalTweets) - 1):
              with open(path+ '/'+   langOfTweets +   '/' + user  + '/' + user + '_tweets_' + str(currentTweetBatch)+ '.json','w') as fou:
               json.dump(tempTweetArray,fou)
                

         print("total final reply tweets")
         print(len(finalReplyTweets))

         for tweet in finalReplyTweets:
           print('reply tweet')
           print(tweet.text)
           with open(path+ '/'+ user  + '/' + user + 'reply_tweets1.json','a') as fou:
            tweet.country = locationOfTweets
            json.dump(tweet._json,fou)
         


        #  print("filtered tweet length")
        #  print(len(user_tweets))

        #  print(engCount)
        #  print(hindiCount)

     def fetchTweetsMaxId(self,user,tweetcount,currentMaxId):
         user_tweets = api.user_timeline(screen_name = user , count = tweetcount , result_type='recent' , max_id = currentMaxId) 
         print("user tweet length with maxid")
         print(len(user_tweets))
         if len(user_tweets)-1 > 0 :
          self.max_id = user_tweets[len(user_tweets)-1].id - 1
         print(self.max_id)
         return user_tweets

     def processTweets(self,user_tweets,langOfTweets):
         filteredTweets = []
        #  filteredTweets = [tweet for tweet in user_tweets if tweet.user.location == "India"]
         filteredTweets = [tweet for tweet in user_tweets if tweet.lang == langOfTweets]
         filteredTweets = [tweet for tweet in filteredTweets if not hasattr(tweet, 'retweeted_status')]
         filteredTweets = [tweet for tweet in filteredTweets if tweet.in_reply_to_status_id is None] 
         print("filtered Tweets")
         print(len(filteredTweets))
         return filteredTweets

     def processReplyTweets(self,sourceTweet,replyTweets,langOfTweets):
         filteredReplyTweets = []
         for tweet in replyTweets:
             if hasattr(tweet, 'in_reply_to_status_id_str'):
                #  print("replyTweet: ")
                #  print(tweet.in_reply_to_status_id_str)
                #  print("sourceTweet: ")
                #  print(sourceTweet.id_str)
                 if (tweet.in_reply_to_status_id_str==sourceTweet.id_str):
                    print("found one tweet")
                    filteredReplyTweets.append(tweet)
        
         filteredReplyTweets = [tweet for tweet in filteredReplyTweets if tweet.lang == langOfTweets]
         filteredReplyTweets = [tweet for tweet in filteredReplyTweets if not hasattr(tweet, 'retweeted_status')] 
         print("processed reply tweets")
         print(len(filteredReplyTweets))
         return filteredReplyTweets



     def fetchTweets(self,user,tweetcount):
         user_tweets = api.user_timeline(screen_name = user , count = tweetcount , result_type='recent') 
         print("user tweet length")
         print(len(user_tweets))
         self.max_id = user_tweets[len(user_tweets)-1].id
         print(self.max_id)
         return user_tweets
        #  user_tweets = self.processTweets(user_tweets,langOfTweets,locationOfTweets)
        
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



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    # l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,  wait_on_rate_limit=True)
    crawlTweets = TweepyCrawlTweets()
    crawlTweets.crawlForThisUser('realDonaldTrump',3200,'en','USA')

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['python', 'javascript', 'ruby'])




            #  currentUserHandleQuery = "from:" + user
        #  user_tweets = api.search(q = currentUserHandleQuery ,lang=langOfTweets,count = tweetcount , result_type='recent' , max_id=1166258743304052737)
        #  txts = []
        #  for status in user_tweets:
        # #    txts.append(json.dumps(status))
        #    print(status._json)
        
        # #  with open('tweet.json', 'w+') as f:
        # #   json.dump(txts, f)

    

        #        tweet.country = locationOfTweets
        #    if idx % 100 == 0 and idx>=100:
        #      currentTweetBatch = currentTweetBatch + 100
        #    with open(path+ '/'+ user  + '/' + user + '_tweets_' + str(currentTweetBatch)+ '.json','a') as fou:
        #     json.dump(tweet._json,fou)