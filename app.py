from flask import Flask, session, request, url_for, redirect, render_template
from utils import twitter, textprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "something"

if __name__ == '__main__':
    app.debug = True
    app.run()
