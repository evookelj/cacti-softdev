#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from os import urandom

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
        c.execute(query, (user, salt, password, "na"))
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
