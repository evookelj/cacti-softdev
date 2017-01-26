from flask import Flask, session, request, url_for, redirect, render_template
from utils import auth, quench, util, twitter
import json

app = Flask(__name__)
app.secret_key = "deal with this later"

@app.route("/", methods=["GET", "POST"])
def home():
    if len(session.keys())==0:
        return render_template('welcome.html')
    else:
        return render_template("dashboard.html", username=session["username"])

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    un = request.form["handle"]

    if request.form["type"] == "register":
        ps1 = request.form["pass1"]
        ps2 = request.form["pass2"]
        regRet = auth.register(un, ps1, ps2)#returns an error/success message
        return render_template("welcome.html", regerror=regRet)

    else:
        pw = request.form["pass"]
        text = auth.login(un, pw)#error message
        if text == "":#if no error message, succesful go back home
            session["username"] = un
            print text
            return redirect(url_for('home'))
        return render_template("welcome.html", logerror=text)


@app.route("/auth/", methods=['POST'])
def oauth():
    url = auth.getRedirectLink()
    if auth.updated(session["username"]):
        return render_template("dashboard.html",
                username=session["username"],
                message = "Already Authenticated!")
    return redirect(url)

@app.route("/callback/", methods=['GET', 'POST'])
def callback():
    new_token = request.args.get('oauth_token')
    #print new_token
    verifier = request.args.get('oauth_verifier')
    #print verifier
    access = auth.getAccessToken(new_token, verifier)
    user = session["username"]
    resp = auth.update(access, user)

    return render_template("dashboard.html", username=user, message = resp)

@app.route("/archive/")
def history():
    if quench.checkArchive(session["username"]):
        info = {"You don't have any tweets yet!": " Quench tweets to build an archive!"}
    info = quench.getData(session["username"])
    return render_template("archive.html", tweets=info)

@app.route("/logout/", methods=['POST'])
def logout():
    session.pop("username")
    return redirect(url_for('home'))

@app.route("/tweet/", methods=['POST'])
def tweet():
    ui=request.form['tweet']
    print "UI: " + str(ui)
    if len(ui)>140 or len(ui) == 0:
            return render_template("dashboard.html", username=session["username"], message="Please enter a potential tweet that fits within the 140 character limit")

    if "quench" in request.form:
        results=quench.quench(session["username"],ui, False)
        opt = results[0]
        data = results[1]
        data_json = json.dumps(data)
        found_tweets = data != []
        return render_template("results.html", message=ui, found_tweets=found_tweets, time=util.fmtTime(opt), tweets=data_json)

    if "tweeter" in request.form:
        if quench.exists(session["username"], ui):
            return render_template("dashboard.html", username=session["username"], message = "You already tweeted that!")
        if not auth.updated(session["username"]):
            return render_template("dashboard.html", username=session["username"], message = "Please authenticate you account first!")

        resp = twitter.update_tweet(ui, session["username"])
        print "UI: " + str(ui)
        print "TYPE: " + str(type(ui))
        return render_template("dashboard.html",
                               username=session["username"],
                               message = resp)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/algo/")
def algo():
    return render_template("algo.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
