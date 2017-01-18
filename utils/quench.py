#from utils
import textprocess, twitter, enchant, pytz, datetime
from sqlite3 import connect

f = "data/quench.db"
db = connect(f)
c = db.cursor()

# TABLE tweets
# TEXT handle, TEXT tweet, INT hr, INT minute

def createTable():
     c.execute("CREATE TABLE tweets (handle TEXT, tweet TEXT, hr INT, minute INT");
     db.commit()
     db.close()

def exists(user, tweet):
     query = "SELECT hr FROM tweets WHERE handle=? and tweet=?"
     c.execute(query, (user, tweet))
     for record in sel:
          db.commit()
          db.close()
          return True
     db.commit()
     db.close()
     return False

def addToTable(user, tweet, hr, minute, weight):
     if not exists(user, tweet):
          query = ("INSERT INTO tweets VALUES (?, ?, ?, ?)")
          c.execute(query, (user, tweet, hr, minute))
     db.commit()
     db.close()

def isEnglish(text):
     d = enchant.Dict("en_US")
     words = text.split(" ")
     return d.check(words[0]) or d.check(words[2])

def calcTime(tweet, hasImage):

     tweetTag = textprocess.tag(tweet)
     tweetPhrase = textprocess.phrase(tweet)
     fromTweet = list(set(tweetTag) | set(tweetPhrase))
     gotten = []
     twitter.addSearchList(fromTweet)
     datas = twitter.get()
     optHr = 0
     optMin = 0
     totWeight = 0
     for data in datas:
          if isEnglish(data['text']):
               weight =  textprocess.relevancyWeight(tweetPhrase, tweetTag, tweet, data['text'], False)
               if weight != 0:
                    gotten.append({
                         'time': data['time'],
                         'weight': weight
                    })
                    optHr += data['time'][0]*weight
                    optMin += data['time'][1]*weight
                    totWeight += weight
     den = totWeight
     return [optHr/den, optMin/den]

def utcToLocal(hr, minute, tz):
     local_tz = pytz.timezone(tz)
     utc_dt = datetime.datetime(2017,01,15,int(hr),int(minute))
     local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
     user_tz = local_tz.normalize(local_dt)
     return [user_tz.hour, user_tz.minute]

def quench(user, tweet, hasImage):
     utcT = calcTime(tweet, hasImage)
     addToTable(user, tweet, utcT[0], utcT[1])
     return utcToLocal(utcT[0], utcT[1], "US/Eastern")

if __name__ == '__main__':
    print quench(user, "Donald Trump will never be my president", False);
