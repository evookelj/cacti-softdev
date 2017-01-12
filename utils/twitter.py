import sqlite3, time
import oauth2 as oauth
import json

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


t = open("tw.txt","r")
keys = t.read().split("\n")
print keys
CONSUMER_KEY = keys[0]
CONSUMER_SECRET = keys[1]
ACCESS_KEY = keys[2]
ACCESS_SECRET = keys[3]
t.close()

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=%23trump&result_type=popular"

def get():
    response, data = client.request(timeline_endpoint)
    
    tweets = json.loads(data)
    data = []
    for tweet in tweets['statuses']:
        data.append(
            {
                'text': tweet['text'],
                'favoriteCount': tweet['favorite_count'],
                'retweeted': tweet['retweeted'],
                'created_at': tweet['created_at']
            }
        )
    print tweet['created_at']

if (__name__ == "__main__"):
    get()
