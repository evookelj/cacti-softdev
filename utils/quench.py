#from utils
import textprocess, twitter

def calcTime(tweet, hasImage):
    fromTweet = list(set(textprocess.tag(tweet)) | set(textprocess.phrase(tweet)))
    for keyword in tweet:
        print keyword
        if " " not in keyword:
            twitter.addSearchTerm(keyword)
            datas = twitter.get()
            for data in datas:
                #print data['text']
                print "\n"

calcTime("Donald Trump will never be my president", False);
