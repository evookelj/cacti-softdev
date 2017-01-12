import sqlite3, time

database = sqlite3.connect('data/database.db')

def tweetExists(id, user):
    c = database.cursor()
    b = c.execute('SELECT id FROM ' + user)
    for chirp in b:
        if chirp[0] == id:
            return True
    return False

def addTweet(id, user, tweet, time):
    c = database.cursor()
    if (not tweetExists(id, user)):
        c.execute("INSERT INTO tweets VALUES (" + id + ", " + user +", " + tweet + ", " + time + ")")
        database.commit()
