import time
from sqlite3 import connect
import oauth2 as oauth
import json
from time import strptime
import urllib
import tweepy
import auth

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
count = 15
addon = "count=%s"%(count)

f = "data/quench.db"

def get_api(info):
    auth = tweepy.OAuthHandler(info['consumer_key'], info['consumer_secret'])
    auth.set_access_token(info['access_token'], info['access_token_secret'])
    return tweepy.API(auth)

def get_tokens(user):
    db = connect(f)
    c = db.cursor()
    query = "SELECT accessToken, secretToken FROM users WHERE user=?"
    info = c.execute(query, (user, ))    
    tokens = []
    for record in info:
        tokens = record
    db.commit()
    db.close()
    return tokens

def update_tweet(tweet, user):
    info = { 
        "consumer_key": CONSUMER_KEY,
        "consumer_secret": CONSUMER_SECRET,
        "access_token": get_tokens(user)[0],
        "access_token_secret": get_tokens(user)[1], 
    }
    
    api = get_api(info)
    status = api.update_status(status = tweet)    
    return "Tweeted!" 

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
    print len(tweets['statuses'])
    for tweet in tweets['statuses']:
        engagement = float(tweet['favorite_count']+tweet['retweet_count'])*100
        engagement /= tweet['user']['followers_count']
        if engagement > 1:
            engagement = 1
        cntns = 'media' in tweet['entities'] or len(tweet['entities']['urls']) > 0
        if engagement > .0099:
            data.append({
                'text': tweet['text'],
                'engagement': engagement,
                'time': formatTwTime(tweet['created_at']),
                'cntns': cntns
            })
    addon = "lang=en&count=%d"%(count)
    return data
