#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from os import urandom
from flask import request
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
    resp, info = client.request(request_token_url, "GET")
    if resp['status'] != "200":
        raise Exception("Error: " + resp['status'])

    resp = json.dumps(resp)
    info = [resp, info]
    info = ';'.join(info)
    request_token = dict(urlparse.parse_qsl(info))

    #print request_token['oauth_token']
    #print request_token['oauth_token_secret']
    #print request_token

    if request_token['oauth_callback_confirmed']:
        return request_token
    else:
        raise Exception("oauth_callback not true")

def getRedirectLink():
    content = { 'oauth_consumer_key': CONSUMER_KEY,
                'oauth_nonce': getRequestToken()['oauth_nonce'],
                'oauth_signature': getRequestToken()['oauth_signature'],
                'oauth_signature_method': "HMAC-SHA1",
                'oauth_timestamp': getRequestToken()['oauth_timestamp'],
                'oauth_token': getRequestToken()['oauth_token'],
                'oauth_version': getRequestToken()['oauth_version'] }

    return authorize_url + "?" + urllib.urlencode(content)

#print getRedirectLink()

def getAccessToken(new_token, verifier):
    request_token = getRequestToken()

    token = oauth.Token(new_token, request_token['oauth_token_secret'])
    token.set_verifier(verifier)
    client = oauth.Client(consumer, token)

    resp, info = client.request(access_token_url, "POST")
    if resp['status'] != "200":
        raise Exception(resp)

    resp = json.dumps(resp)
    info = [resp, info]
    info = ';'.join(info)
    access_token = dict(urlparse.parse_qsl(info))

    #print access_token
    #print access_token['oauth_token']
    #print access_token['oauth_token_secret']

    return [access_token['oauth_token'], access_token['oauth_token_secret']]

f = "data/quench.db"
db = connect(f)
c = db.cursor()

def login(user, password):
    db = connect(f)
    c = db.cursor()

    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, accessToken TEXT, secretToken TEXT)")

    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));

    #records with this username
    #so should be at most one record (in theory)

    for record in sel:
        password = sha1(password+record[1]).hexdigest()##record[1] is the salt
        if (password==record[2]):
            return "" #no error message because it will be rerouted to mainpage
        else:
            return "User login has failed. Invalid password" #error message
        db.commit()
        db.close()
    return "Username does not exist" #error message

def register(user, ps1, ps2):
    if not ps1 == ps2:
        return "Passwords not the same."
    db = connect(f)
    c = db.cursor()
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
        db.commit()
        db.close()
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, accessToken TEXT, secretToken TEXT)")
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
        query = ("INSERT INTO users VALUES (?, ?, ?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user, salt, password, "tbd", "tbd"))
        db.commit()
        db.close()
        return "Account created!"
    db.commit()
    db.close()
    return reg#return error message

def update(tokens, user):
    resp = verify(tokens)

    db = connect(f)
    c = db.cursor()
    if resp == "": # no error message means db can be updated
        query = ("UPDATE users SET accessToken=?, secretToken=? WHERE user=?")
        c.execute(query, (tokens[0], tokens[1], user))
        db.commit()
        db.close()
        return "account authenticated!"
    db.commit()
    db.close()
    return resp

def updated(user): #checks if the account is already authenticated

    db = connect(f)
    c = db.cursor()
    query = ("SELECT accessToken, secretToken FROM users WHERE user =?")
    result = c.execute(query, (user, ))
    for sel in result:
        if sel[0] == 'tbd':
            return False
    db.commit()
    db.close()
    return True

def verify(tokens): #error message for tokens
    if not tokens:
        return "Authentication Unsuccessful"
    if len(tokens) == 1:
        return "Missing Tokens to authenticate"
    return ""

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

db.commit()
db.close()

if __name__ == '__main__':
    getRequestToken()
    getRedirectLink()
    getCallbackInfo()
    getAccessToken()
