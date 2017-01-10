import urllib2, json, requests 

def sentiment(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/sentiment/",data=data)
    return r.json()

def stem(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/stem/",data=data)
    return r.json()

def phrase(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/phrases/",data=data)
    return r.json()

def tag(text):
    data={ 'text':text}
    r = requests.post("http://text-processing.com/api/tag/",data=data)
    return r.json()

print sentiment("good")
print stem("lovely")
print phrase("Red velvet brownies")
print tag("computer science")
