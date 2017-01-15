from flask import Flask, session, request, url_for, redirect, render_template
from utils import auth

app = Flask(__name__)
app.secret_key = "deal with this later"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # TODO: Actually login/register
        if 'form' in request.form:
            return 'Invalid request.'
        elif request.form['type'] == 'login':
            return 'Login functionality <em>coming soon!</em>'
        elif request.form['type'] == 'register':
            return 'Register functionality <em>coming soon!</em>'
    return render_template('welcome.html')

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    un = request.form["handle"]
    
    if request.form["type"] == "register":
        ps1 = request.form["pass1"]
        ps2 = request.form["pass2"]
        regRet = auth.register(un,ps1,ps2)#returns an error/success message
        print regRet
        return redirect(url_for('home'))
        
    else:
        pw = request.form["pass"]
        text = auth.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["username"] = un
            print text
            return redirect(url_for('home'))
        print text
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.debug = True
    app.run()
