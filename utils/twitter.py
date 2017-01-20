import sqlite3, time
import oauth2 as oauth
import json
from time import strptime
import urllib

t = open("tw.txt","r")
keys = t.read().split("\n")
CONSUMER_KEY = keys[0]
CONSUMER_SECRET = keys[1]
ACCESS_KEY = keys[2]
ACCESS_SECRET = keys[3]
t.close()

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?"
count = 20
addon = "lang=en&count=%d"%(count)




def addSearchTerm(term):
    global addon
    pre = "&q="
    addon += urllib.quote_plus(pre + term)

def addSearchList(list):
    global addon
    pre = "&q="
    these = list[0]
    first = True
    for word in list:
        if first:
            first = False
        else:
            these += " OR %s"%(word)
    these = urllib.quote_plus(these)
    addon += pre + these

def formatTwTime(twTime):
    time = twTime.split(" ")[3].split(":")
    hr = int(time[0])
    minute = int(time[1])
    return [hr, minute]
    
def get():
    global addon
    addon += "&result_type=popular"
    url = timeline_endpoint+addon
    response, data = client.request(url)
    print "URL: " + url
    tweets = json.loads(data)
    data = []
    if 'errors' in tweets.keys():
        print tweets['errors'][0]['message']
        return []
    for tweet in tweets['statuses']:
        engagement = float(tweet['favorite_count']+tweet['retweet_count'])
        engagement /= tweet['user']['followers_count']
        if engagement > .099:
            data.append({
                'text': tweet['text'],
                'engagement': engagement
                'time': formatTwTime(tweet['created_at'])
            })
    addon = "lang=en&count=%d"%(count)
    return data

if (__name__ == "__main__"):
    addSearchTerm("puppy");
    get()

