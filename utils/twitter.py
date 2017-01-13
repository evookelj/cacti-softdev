import sqlite3, time
import oauth2 as oauth
import json
from datetime import datetime
from time import strptime

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
addon = ""

def addSearchTerm(term):
    global addon
    if addon=="":
        pre = "q=%23"
    else:
        pre = "&q=%23"
    addon += pre + term

def formatTwTime(twTime):
    twTime = twTime.split(" ")
    time = twTime[3].split(":")
    yr = int(twTime[-1])
    mon = strptime(twTime[1],'%b').tm_mon
    day = int(twTime[2])
    hr = int(time[0])
    minute = int(time[1])
    sec = int(time[2])
    t = datetime(yr, mon, day, hr, minute, sec)
    return t
    
def get():
    global addon
    addon += "&result_type=popular"
    url = timeline_endpoint+addon
    response, data = client.request(url)
    print url
    
    tweets = json.loads(data)
    data = []
    if 'errors' in tweets.keys():
        print tweets['errors'][0]['message']
    for tweet in tweets['statuses']:
        data.append({
                'text': tweet['text'],
                'favoriteCount': tweet['favorite_count'],
                'retweeted': tweet['retweeted'],
                'time': formatTwTime(tweet['created_at'])
            })
    addon = ""

if (__name__ == "__main__"):
    addSearchTerm("puppy");
    get()

#database = sqlite3.connect('data/database.db')

def tweetExists(id, user):
    c = database.cursor()
    b = c.execute('SELECT id FROM ' + user)
    for chirp in b:
        if chirp[0] == id:
            return True
    return False

def addTweet(id, user, tweet, time):
    c = database.cursor()
    if (not tweetExists(id, user)):
        c.execute("INSERT INTO tweets VALUES (" + id + ", " + user +", " + tweet + ", " + time + ")")
        database.commit()
