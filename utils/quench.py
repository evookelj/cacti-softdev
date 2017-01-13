#from utils
import textprocess, twitter, enchant

def isEnglish(text):
     d = enchant.Dict("en_US")
     words = text.split(" ")
     try:
         return d.check(words[0]) and d.check(words[2]) and d.check(words[4])
     except:
         return False

def getData(tweet, hasImage):
    fromTweet = list(set(textprocess.tag(tweet)) | set(textprocess.phrase(tweet)))
    ret = []
    for keyword in tweet:
        if " " not in keyword:
            twitter.addSearchTerm(keyword)
            datas = twitter.get()
            for data in datas:
                if isEnglish(data['text']):
                    ret.append({
                        'time': data['time'],
                        'weight': textprocess.relevancyWeight(tweet, data['text'], False)
                    })
        print "a word"
    return ret

print getData("Donald Trump will never be my president", False);
