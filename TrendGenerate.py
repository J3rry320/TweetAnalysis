import json

import tweepy
import sys
from pprint import pprint
import config
configOperators = config.config
nameOfPerson=input("Give The Name of the person You Want To Search For")
auth = tweepy.OAuthHandler(
    configOperators["consumer_key"], configOperators["consumer_secret"])
auth.set_access_token(
    configOperators["access_key"], configOperators["access_secret"])
api = tweepy.API(auth)
trends = api.trends_place(23424848)
trends_available = api.trends_available()
print(type(trends))
CountryData = {}
for a, b in enumerate(trends_available):
  CountryData["country"+str(a)] = b["country"]
  CountryData["woeid"+str(a)] = b["woeid"]

final=[]

for tweet in tweepy.Cursor(api.search,
                           q=nameOfPerson,
                           count=100,

                           lang="en",
                           tweet_mode='extended').items(500):


    query_list={

        "time":tweet.created_at,
        "tweet":tweet.full_text.encode('ascii',"ignore").rstrip(),
        "retweets":tweet.retweet_count,
        "followers":tweet.user._json["followers_count"],
        "hashtags":tweet.entities["hashtags"],
        "screenName":tweet.user._json["screen_name"],
        "description":tweet.user._json["description"].encode('ascii',"ignore").rstrip()

       }


    final.append(query_list)
    tweetfile = open("tweets.json", "w+")
    tweetfile.truncate()
    tweetfile.write(json.dumps(final, indent=4,
                                default=str))
    tweetfile.close()




LocationJson = open("location.json", "w+")
LocationJson.truncate()
LocationJson.write(json.dumps(CountryData))
LocationJson.close()


jsonFile = open("trends.json", "w+")
jsonFile.truncate()
jsonFile.write(json.dumps(trends))
jsonFile.close()


# Import the necessary package to process data in JSON format
