from flask import redirect, render_template, request, session
from app import app
from db import db
import users
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    return render_template("index.html",error = False)

@app.route("/login",methods=["POST"])
def login():
    value = users.login()
    if value == "not_user":
        return render_template("index.html", error = "Incorrect username")
    if value == True:
        return render_template("index.html",error=False)
    else:
        return render_template("index.html", error ="Incorrect  password")
@app.route("/signin",methods=["POST"])
def signin():
    if users.register() == 1:
        return render_template("index.html",signup =True)
    else:
        return render_template("index.html",error="Something went wrong")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/form/cardio")
def form_cardio():
    return render_template("form/cardio.html")

@app.route("/form/gym")
def form_gym():
    return render_template("form/gym.html")

@app.route("/choice")
def choice():
    try:
        if len(session["username"]) > 0:
            return render_template("choice.html")
        return render_template("choice.html")
    except:
        return render_template("index.html", error="You need to login to continue")

@app.route("/addexercise",methods=["POST"])
def addexercise():
    value = users.add_gym()
    if value == False :
        return render_template("index.html", added=True)
    else:
        return render_template("form/gym.html", exercises=value)

@app.route("/profile/<int:id>")
def profile(id):
    #first we get the visit id.
    allexercises = users.show_exercises(id)
    return render_template("profile.html", allexercises=allexercises)