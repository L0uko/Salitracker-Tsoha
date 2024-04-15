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
    username = request.form["username"]
    password = request.form["password"]
    
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("index.html", error = "Incorrect username")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"]  = users.find_user_id(username)
            return render_template("index.html",error=False)
        else:
            return render_template("index.html", error ="Incorrect  password")

    return redirect("/")

@app.route("/signin",methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 1:
        return render_template("index.html",error="Username was too short")
    if len(password) < 1:
        return render_template("index.html",error="Password was too short")
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return render_template("index.html",signup =True)
    except:
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
    exercisename = request.form["exercisename"]
    sets   = request.form["sets"]
    weight = request.form["weight"]
    date   = request.form["date"]
    username= session["username"]
    user_id= users.find_user_id(username)
    sql    = text('''INSERT INTO exercise (sets, weight, exercisename)
                  VALUES (:sets, :weight, :exercisename) RETURNING id''')
    result = db.session.execute(sql, {"sets":sets, "weight":weight, "exercisename":exercisename }).fetchone()
    result=result[0]
    sql    =text('''INSERT INTO visits (date, user_id, exercise_id) VALUES (:date, :user_id, :exercise_id) RETURNING id''')
    result = db.session.execute(sql, {"date":date, "user_id":user_id, "exercise_id":result}).fetchone()
    db.session.commit()
    visit_id = result[0]
    if request.form["Continue"] == "True":
        return render_template("form/gym.html", exercises=exercisename)
    else:
        return render_template("index.html", added=True)

@app.route("/profile/<int:id>")
def profile(id):
    #first we get the visit id.
    #sql = text("SELECT v.id, v.date, v.exercise_id")
    sql = text("SELECT exercise.id, exercise.sets  FROM exercise, users, visits WHERE exercise.id=visits.exercise_id")
    exercises= db.session.execute(sql,{"exercise.id":id}).fetchall()
    print(exercises)
    return render_template("profile.html")