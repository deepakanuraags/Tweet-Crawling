import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
import time


class TweetCount:
    def countTweetsForLanguage(self,lang):
        users = os.listdir(os.getcwd() + '/' + lang)
        print(users)
        totalTweetCount = 0 
        totalReplyCountForAllUsers = 0
        totalReplyCountForUser = 0
        for user in users:
            print('in for loop')
            shouldBreak = False
            currentCount = 0
            while shouldBreak == False:
              print('in while loop')
              if not os.path.exists(os.getcwd()+ '/'+  lang +'/' + user + '/'+ user  + '_tweets_' + str(currentCount + 100) + '.json'):
                  print(os.getcwd()+ '/'+  lang +'/' + user + '/'+ user  + '_tweets_' + str(currentCount + 100))
                  shouldBreak = True
                  print('while broke')
                  totalTweetCount = totalTweetCount + currentCount
                  print('tweet for user : ' + user + ' : ' + str(currentCount))
                  print('total tweet for language : ' + str(totalTweetCount))
              else :
                  currentCount = currentCount + 100
                  print('in else ' + str(currentCount))
              
              os.listdir(

            totalReplyCountForUser = 0
            if os.path.exists(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets'):
              
              reply_list_files = os.listdir(os.getcwd() + '/' + lang + '/' + user + '/' + 'replyTweets')

              for file in reply_list_files:
                   print(file)
                   startCharpos = self.charposition(file,'_')
                   endCharPos = self.charposition(file,'.')
                   if(startCharpos+1>-1 and endCharPos>startCharpos):
                     countStr = file[startCharpos+1:endCharPos]
                     intCount = int(countStr)
                     print('replyCount : ' + str(intCount))
                     totalReplyCountForUser = totalReplyCountForUser + intCount

              print('total reply count for ' + user + ' :' + str(totalReplyCountForUser))
            
            totalReplyCountForAllUsers = totalReplyCountForAllUsers +  totalReplyCountForUser
            print('total tweet count for all users ' + str(totalTweetCount))
            print('total reply count for all users ' + str(totalReplyCountForAllUsers))
            print('total tweet count : ' + str(totalTweetCount + totalReplyCountForAllUsers))

    def countTweets(self,lang):
      users = os.listdir(os.getcwd() + '/' + lang))
      totalTweetsCounter = 0
      for user in users:
        files =  os.listdir(os.getcwd() + '/' + lang + '/' + user)

 
        for file in files:
          print(file)
          if(startCharpos+1>-1 and endCharPos>startCharpos):
                     countStr = file[startCharpos+1:endCharPos]
                     intCount = int(countStr)
                     print('file : ' + + str(intCount))
                     totalTweetsCounter = totalTweetsCounter + intCount
          



    def charposition(self,string, char):
      pos = [] #list to store positions for each 'char' in 'string'
      for n in range(len(string)):
        if string[n] == char:
            pos.append(n)
      if len(pos)>0:
       return pos[len(pos) - 1]
      else:
       return -1


if __name__ == '__main__':

    countTweets = TweetCount()
    countTweets.countTweetsForLanguage('pt')



              
