from flask import Flask, session, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
