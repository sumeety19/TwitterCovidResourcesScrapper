import tweepy
from textblob import TextBlob
import jsonpickle
import pandas as pd
import json

CONSUMER_KEY = "0GHBBLM1BImXSmUVI5hQP1bou"
CONSUMER_SECRET = "a5OxetJT9q2jJFD5E8Jo0X8YGe88vgj0MaxLnJUc8tzA5jgtBp"
ACCESS_KEY = "61354924-E7l18ch4TOtARLGBAEJqRjg6SnM0mXOEAlEh4tEdX"
ACCESS_SECRET = "P5P096kCzSzX3Kab4uHxULVar4Jfpmi9oKHQjPOyKaEhq"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

searchQuery = 'Oxygen Beds India' or 'Covid Resources India' or 'covid resources'
retweet_filter='-filter:retweets'
q=searchQuery #+retweet_filter
tweetsPerQry = 100
fName = 'tweets.txt'
sinceId = None

max_id = -1
maxTweets = 100

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        tweets = []
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=q, lang ="en", count=tweetsPerQry, tweet_mode='extended')

                else:
                    new_tweets = api.search(q=q, lang ="en", count=tweetsPerQry,
                                        since_id=sinceId, tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=q, lang ="en", count=tweetsPerQry,
                                        max_id=str(max_id - 1), tweet_mode='extended')
                else:
                    new_tweets = api.search(q=q, lang ="en", count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId, tweet_mode='extended')

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(str(tweet.full_text.replace('\n','').encode("utf-8"))+"\n")

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
                
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
                
print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))