#from utils
import textprocess, twitter, enchant, pytz, datetime

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

def quench(tweet, hasImage):
     utcT = calcTime(tweet, hasImage)
     return utcToLocal(utcT[0], utcT[1], "US/Eastern")

print quench("Donald Trump will never be my president", False);
