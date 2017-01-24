#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from os import urandom
import oauth2 as oauth
import urllib, urllib2
import urlparse
import json

t = open("tw.txt","r")
keys = t.read().split("\n")
CONSUMER_KEY = keys[0]
CONSUMER_SECRET = keys[1]
ACCESS_KEY = keys[2]
ACCESS_SECRET = keys[3]
t.close()

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

def getRequestToken():
    info = client.request(request_token_url, "GET")
    info = list(info)
    info[0] = json.dumps(info[0])
    info = ';'.join(info)
    request_token = dict(urlparse.parse_qsl(info))
    #print request_token['oauth_token']
    #print request_token['oauth_token_secret']
    print request_token
    return request_token

def getRequestLink(): 
    return authorize_url + "?oauth_token=%s"%(getRequestToken()['oauth_token'])

def getAccessToken():
    '''
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')
    '''

    request_token = getRequestToken()
    token = oauth.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
    #token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    info = client.request(access_token_url, "POST")
    info = list(info)
    info[0] = json.dumps(info[0])
    info = ';'.join(info)
    access_token = dict(urlparse.parse_qsl(info))
    print "break"
    print access_token
    print access_token['oauth_token_secret']

    return access_token
'''
def getAccessLink():

    content = { oauth_consumer_key = CONSUMER_KEY,
                oauth_nonce = getRequestToken()['oauth_nonce'],
                oauth_signature = getRequestToken()['oauth_signature'],
                oauth_signature_method = "HMAC-SHA1",
                oauth_timestamp = getRequestToken()['date'],
                oauth_token = getRequestToken()['oauth_token']
                oauth_version = "1.0"
                oauth_callback = }

    print authorize_url + "?" + urllib.urlencode(content)
    
    return authorize_url + "?" + urllib.urlencode(content)

f = "data/quench.db"
db = connect(f)
c = db.cursor()

def login(user, password):
    db = connect(f)
    c = db.cursor()

    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, clientToken TEXT)")

    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));

    #records with this username
    #so should be at most one record (in theory)

    for record in sel:
        password = sha1(password+record[1]).hexdigest()##record[1] is the salt
        if (password==record[2]):
            return ""#no error message because it will be rerouted to mainpage
        else:
            return "User login has failed. Invalid password"#error message
        db.commit()
        db.close()
    return "Username does not exist"#error message

def register(user, ps1, ps2):
    if not ps1 == ps2:
        return "Passwords not the same."
    db = connect(f)
    c = db.cursor()
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, clientToken TEXT)")
        db.commit()
        db.close()
    return regMain(user, ps1)#register helper

def regMain(user, password):#register helper
    db = connect(f)
    c = db.cursor()
    reg = regReqs(user, password)
    if reg == "": #if error message is blank then theres no problem, update database
        salt = urandom(10).encode('hex')
        print salt
        query = ("INSERT INTO users VALUES (?, ?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user, salt, password, getAccessToken()['oauth_token']))
        db.commit()
        db.close()
        return "Account created!"
    db.commit()
    db.close()
    return reg#return error message

def regReqs(user, password):      #error message generator
    if len(password) < 8 or len(password) > 32:
        return "Password must be 8-32 characters"
    if len(user) < 8 or len(user) > 32:
        return "Username must be 8-32 characters"
    if duplicate(user):          #checks if username already exists
        return "Username already exists"
    if " " in user or " " in password:
        return "Spaces not allowed in user or password"
    if user==password:
        return "Username and password must be different"
    return ""

def duplicate(user):#checks if username already exists
    db = connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (user,))
    retVal = False
    for record in sel:
        retVal = True
        db.commit()
        db.close()
    return retVal
'''

if __name__ == '__main__':
    getRequestToken()
    getAccessToken()
