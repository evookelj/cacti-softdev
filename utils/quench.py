#from utils
import textprocess, twitter

def calcTime(tweet, hasImage):
    fromTweet = list(set(textprocess.tag(tweet)) | set(textprocess.phrase(tweet)))
    for keyword in tweet:
        if " " not in keyword:
            twitter.addSearchTerm(keyword)
            datas = twitter.get()
            for data in datas:
                print data['text']

calcTime("Donald Trump will never be my president", False);
