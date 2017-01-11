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
    return r.json()['text']#.split(" ")

def isSameSentiment(userGiven, foundTweet):
    senUser = sentiment(userGiven)
    senTweet = sentiment(foundTweet)
    eps = .2
    if abs(senUser['neg']-senTweet['neg']) > eps:
        return False
    if abs(senUser['pos']-senTweet['pos']) > eps:
        return False
    return True

def isRelevant(userGiven, foundTweet):
    #the below should be removed once twitter api takes phrase data
    #from given post in query str. this is just here for testing
    phraseUser = phrase(userGiven)
    phraseTweet = phrase(foundTweet)
    if len(list(set(userGiven) & set(foundTweet))) == 0:
        return False
    #end of code just for testing before ready
    
    return isSameSentiment(userGiven, foundTweet)
    
"""
print sentiment("good")
print stem("Life is amazing and silly")
print phrase("Red velvet brownies")
print tag("computer science and english are so different")
"""
print isRelevant("I love belle and sebastian","belle and sebastian are the best!")
print isRelevant("I love belle and sebastian","belle and sebastian are the worst!")
