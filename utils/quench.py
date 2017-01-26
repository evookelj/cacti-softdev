#from utils
import textprocess, twitter, pytz, datetime
from utils import util
from sqlite3 import connect

f = "data/quench.db"

# TABLE tweets
# TEXT handle, TEXT tweet, INT hr, INT minute, results TEXT, posted TEXT

def checkCreateTable():
     db = connect(f)
     c = db.cursor()
     try:
          c.execute("SELECT * FROM tweets")
     except:
          c.execute("CREATE TABLE tweets (handle TEXT, tweet TEXT, hr INT, minute INT, results TEXT, posted TEXT)");
     db.commit()
     db.close()

def exists(user, tweet):
     db = connect(f)
     c = db.cursor()
     checkCreateTable()
     query = "SELECT hr FROM tweets WHERE handle=? and tweet=? AND posted=?"
     sel = c.execute(query, (user, tweet, "True"))
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
          query = ("INSERT INTO tweets VALUES (?, ?, ?, ?, ?, ?)")
          c.execute(query, (user, tweet, hr, minute, "na", "False"))
     db.commit()
     db.close()

def getTime(user, tweet):
     db = connect(f)
     c = db.cursor()
     checkCreateTable()
     query = "SELECT hr, minute FROM tweets WHERE handle=? and tweet=?"
     info = c.execute(query, (user, tweet[0]))
     time = []
     for record in info:
          time = record
     print time
     db.commit()
     db.close()
     return time

def checkArchive(user):
     db = connect(f)
     c = db.cursor()
     checkCreateTable()
     query = "SELECT tweet FROM tweets WHERE handle=?"
     info = c.execute(query, (user,))
     len = 0
     for tweet in info:
          len += 1
     db.commit()
     db.close()
     return len == 0

def getData(user):
     db = connect(f)
     c = db.cursor()
     checkCreateTable()
     query = "SELECT tweet FROM tweets WHERE handle=?"
     info = c.execute(query, (user,))
     data = {}
     for tweet in info:
          gt = getTime(user, tweet)
          tm = utcToLocal(gt[0], gt[1], "US/Eastern")
          if len(tm) == 0:
               tm = ("00","00")
          tweet = str(tweet[0])
          data[tweet]= str(tm[0]) + ":" + str(tm[1])
     db.commit()
     db.close()
     return data

def isEnglish(text):
     d = enchant.Dict("en_US")
     words = text.split(" ")
     return d.check(words[0]) or d.check(words[2])

def calcTime(tweet, hasImage):

     tweetTag = textprocess.tag(tweet)
     tweetPhrase = textprocess.phrase(tweet)
     fromTweet = tweetPhrase
     gotten = []
     twitter.addSearchList(fromTweet)
     datas = twitter.get()
     optHr = 0
     optMin = 0
     totWeight = float(0)
     for data in datas:
          wordWeight =  textprocess.relevancyWeight(tweetPhrase, tweetTag, tweet, data['text'], False)
          if wordWeight != 0:
               engagement = data['engagement']
               weight = float((wordWeight*.5) + (engagement*.5))
               gotten.append({
                    'time': utcToLocal(data['time'][0], data['time'][1], "US/Eastern"),
                    'weight': weight
               })
               optHr += data['time'][0]*weight
               optMin += data['time'][1]*weight
               totWeight += float(weight)
               print "GOT ONE"
     if totWeight != 0:
          return [[int(optHr/totWeight), int(optMin/totWeight)], gotten]
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
     result = [ utcToLocal(utcT[0], utcT[1], "US/Eastern"), clc[1] ]
     addToTable(user, tweet, utcT[0], utcT[1])
     print result
     return result
