from flask import Flask, session, request, url_for, redirect, render_template
from utils import auth, quench, util
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

@app.route("/tweeter/", methods=['POST'])
def tweetForMe():
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout/", methods=['POST'])
def logout():
    session.pop("username")
    return redirect(url_for('home'))

@app.route("/tweet/", methods=['POST'])
def tweet():
    if not 'tweet' in request.form:
        return render_template("dashboard.html",username=session["username"], message = "Please write a tweet!")
    ui=request.form['tweet']
    if len(ui)>140:
        return render_template("dashboard.html", username=session["username"], message="Please enter a potential tweet that fits within the 140 character limit")
    results=quench.quench(session["username"],ui, False)
    opt = results[0]
    data = results[1]
    data_json = "[]"
    try:
        data_json = json.dumps(data)
    except:
        print "ERROR!: json.dumps(data) failed. Data was:"
        print data
        print "Falling back by sending \"[]\" (so there will be an empty graph"
    #return render_template("results.html", message=ui, time=util.fmtTime(opt), tweets=data_json)
    return render_template("results.html", message=ui, time=opt, tweets=data_json)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/algo/")
def algo():
    return render_template("algo.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
