#from utils
import textprocess, twitter, enchant, pytz, datetime
from sqlite3 import connect

f = "data/quench.db"

# TABLE tweets
# TEXT handle, TEXT tweet, INT hr, INT minute

def checkCreateTable():
     db = connect(f)
     c = db.cursor()
     try:
          c.execute("SELECT * FROM tweets")
     except:
          c.execute("CREATE TABLE tweets (handle TEXT, tweet TEXT, hr INT, minute INT)");
     db.commit()
     db.close()

def exists(user, tweet):
     db = connect(f)
     c = db.cursor()
     query = "SELECT hr FROM tweets WHERE handle=? and tweet=?"
     sel = c.execute(query, (user, tweet))
     retVal = False
     for record in sel:
          retVal = True
     db.commit()
     db.close()
     return retVal

def addToTable(user, tweet, hr, minute):
     db = connect(f)
     c = db.cursor()
     checkCreateTable()
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
     totWeight = float(0)
     for data in datas:
          if isEnglish(data['text']):
               wordWeight =  textprocess.relevancyWeight(tweetPhrase, tweetTag, tweet, data['text'], False)
               if wordWeight != 0:
                    engagement = data['engagement']
                    weight = float((wordWeight*.5) + (engagement*.5))
                    print "Time: " + str(data['time'])
                    print "Weight: " + str(weight) + "\n"
                    gotten.append({
                         'time': data['time'],
                         'weight': weight
                    })
                    optHr += data['time'][0]*weight
                    optMin += data['time'][1]*weight
                    totWeight += float(weight)
     den = totWeight#*len(gotten)
     print "den: %d"%(den)
     if den != 0:
          return [[int(optHr/den), int(optMin/den)], gotten]
     else:
          return [ [0,0], gotten ]

def utcToLocal(hr, minute, tz):
     local_tz = pytz.timezone(tz)
     utc_dt = datetime.datetime(2017,01,15,int(hr),int(minute))
     local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
     user_tz = local_tz.normalize(local_dt)
     return [user_tz.hour, user_tz.minute]

def quench(user, tweet, hasImage):
     clc = calcTime(tweet, hasImage)
     utcT = clc[0]
     addToTable(user, tweet, utcT[0], utcT[1])
     tm = [ utcToLocal(utcT[0], utcT[1], "US/Eastern"), clc[1] ]
     return tm

if __name__ == '__main__':
     quench("user", "Donald Trump will never be my president", False);
