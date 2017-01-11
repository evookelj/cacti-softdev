import json, requests , math

def sentiment(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/sentiment/",data=data)
    return r.json()['probability']

def stem(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/stem/",data=data)
    return r.json()['text']

def phrase(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/phrases/",data=data)
    return r.json()['NP']

def tag(text):
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

def isSameTopic(userGiven, foundTweet, isMoreSensitive):
    phraseUser = phrase(userGiven)
    phraseTweet = phrase(foundTweet)
    if len(list(set(userGiven) & set(foundTweet))) > 0:
        return True

    #check tagging b/c desp to find similarity
    tagUser = tag(userGiven)
    tagTweet = tag(foundTweet)
    return isSameChunks(tagUser, tagTweet, isMoreSensitive)

def isSameChunks(tagUser, tagTweet, isMoreSensitive):
    if isMoreSensitive:
        sim = 3
    else:
        sim = 1
    return len(list(set(tagUser) & set(tagTweet))) >= sim

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
    return max(1-negDiff, 1-posDiff)

#use isMoreSensitive to be less sensitive to sentiment-relatability in case
#not enough data to be super harsh about that
def relevancyWeight(userGiven, foundTweet, isMoreSensitive):
    if not isSameTopic(userGiven, foundTweet, isMoreSensitive):
        return 0
    return isSameSentiment(userGiven, foundTweet, isMoreSensitive)
    
print relevancyWeight("I love belle and sebastian","belle and sebastian are the worst!", False)
print relevancyWeight("Belle and sebastian are okay", "I love belle and sebastian", False)
