import json, requests , math

def sentiment(text):
    text = text.lower()
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/sentiment/",data=data)
    return r.json()['probability']

def stem(text):
    text = text.lower()
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/stem/",data=data)
    return r.json()['text']

def phrase(text):
    text = text.lower()
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/phrases/",data=data)
    return r.json()['NP']

def tag(text):
    text = text.lower()
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/tag/",data=data)
    resp = r.json()['text'][3:].split("\n")
    for chunk in resp:
        chunk = chunk.strip()
    if len(resp)==1:
        resp = resp[0].split(" ");

    #NN's and VBG's are the most important words (idk what stand for)
    ret = []
    for chunk in resp:
        if 'NN' in chunk[-3:]:
            ret.append(stem(chunk[:-2].strip(" \/N")))
        if 'VBG' in chunk[-4:]:
            ret.append(stem(chunk[:-3].strip(" \/N")))
    return ret

def isSameTopic(phraseUser, tagUser, foundTweet, isMoreSensitive):
    phraseTweet = phrase(foundTweet)
    intrs = len(list(set(phraseUser) & set(phraseTweet)))
    if intrs==0:
        return 0
    den = .95*(len(phraseUser) + len(phraseTweet))+.05
    phrVal = float(intrs)/den
    tagTweet = tag(foundTweet)
    print "GOT IS SAME TOPIC"
    
    return (.8*phrVal)+(.2*isSameChunks(tagUser, tagTweet, isMoreSensitive))

def isSameChunks(tagUser, tagTweet, isMoreSensitive):
    if isMoreSensitive:
        sim = 3
    else:
        sim = 1
    intrs = len(list(set(tagUser) & set(tagTweet)))
    if intrs==0:
        intrs = .1
    den = .95*(len(tagUser) + len(tagTweet))+.05
    retVal = float(intrs)/den
    print "GOT IS SAME CHUNKS"
    return retVal

def isSameSentiment(userGiven, foundTweet, isMoreSensitive):
    senUser = sentiment(userGiven)
    senTweet = sentiment(foundTweet)
    eps = .2
    if isMoreSensitive:
        eps = .1

    negDiff = abs(senUser['neg'] - senTweet['neg'])
    posDiff = abs(senUser['pos'] - senTweet['pos'])
    if negDiff > eps:
        return 0
    if posDiff > eps:
        return 0
    retVal = max(1-negDiff, 1-posDiff)
    print "GOT IS SAME SENTIMENT"
    return retVal

#use isMoreSensitive to be less sensitive to sentiment-relatability in case
#not enough data to be super harsh about that
def relevancyWeight(phraseUser, tagUser, userGiven, foundTweet, isMoreSensitive):
    userGiven = userGiven.lower()
    foundTweet = foundTweet.lower()
    retVal = ((.2*isSameTopic(phraseUser, tagUser, foundTweet, isMoreSensitive)) + (.8*isSameSentiment(userGiven, foundTweet, isMoreSensitive)))*1.1
    print "GOT RELEVANCY"
    return retVal

if __name__ == '__main__':
    print " "
