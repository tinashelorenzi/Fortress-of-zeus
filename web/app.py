from flask import Flask, render_template,redirect,session,request
import firebase_handler as firebase_handler
import driver as handler

app = Flask(__name__)
app.secret_key = "WeWillBeChosenForTheDaysOfWar"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def authenticate():
    username = request.form["userid"]
    password = request.form["password"]
    print("userid", username, "password", password)
    if username == "admin" and password == "admin":
        session["username"] = username
        return redirect("/main")
    else:
        return render_template("index.html", error="Invalid username or password")
    
@app.route("/main")
def main():
    if "username" in session:
        app_codes = handler.get_data_from_firebase()
        return render_template("main.html",app_codes=app_codes)
    else:
        return redirect("/")
    
@app.route("/get_app_codes")
def fetch_codes():
    app_codes = handler.get_data_from_firebase()
    return app_codes