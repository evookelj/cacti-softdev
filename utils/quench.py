#from utils
import textprocess, twitter, enchant

def isEnglish(text):
     d = enchant.Dict("en_US")
     words = text.split(" ")
     return d.check(words[0]) or d.check(words[2])

def getData(tweet, hasImage):

     tweetTag = textprocess.tag(tweet)
     tweetPhrase = textprocess.phrase(tweet)
     fromTweet = list(set(tweetTag) | set(tweetPhrase))
     gotten = []
     twitter.addSearchList(fromTweet)
     datas = twitter.get()
     optHr = 0
     optMin = 0
     for data in datas:
          if isEnglish(data['text']):
               weight =  textprocess.relevancyWeight(tweetPhrase, tweetTag, tweet, data['text'], False)
               gotten.append({
                    'time': data['time'],
                    'weight': weight
                         })
               optHr += data['time'][0]*weight
               optMin += data['time'][1]*weight
     #print len(gotten)
     return [optHr/len(gotten), optMin/len(gotten)]

print getData("Donald Trump will never be my president", False);
