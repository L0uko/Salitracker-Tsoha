from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

#How to make new image and run server:
#docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server

#Run these 2 commands in different terminals in this order to start the database
#docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name  -p 5432:5432
#docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

'''TODOLIST:
TODO more tables (dont know how)
TODO profile sort by time exercises
TODO Running
TODO route where can choose between running and gym 
(maybe 3rd option? sport?)
TODO Profile see all exercises
TODO Templates?(new tables?)
'''
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


 
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
            session["user_id"]  = find_user_id(username)
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


@app.route("/form")
def form():
    try:
        if len(session["username"]) > 0:
            return render_template("form.html")
        return render_template("form.html")
    except:
        return render_template("index.html", error="You need to login to continue")

@app.route("/addexercise",methods=["POST"])
def addexercise():    
    exercisename = request.form["exercisename"]
    sets   = request.form["sets"]
    weight = request.form["weight"]
    time   = request.form["time"]
    username= session["username"]
    user_id= find_user_id(username)
    sql    = text('''INSERT INTO exercise (sets, weight, exercisename)
                  VALUES (:sets, :weight, :exercisename) RETURNING id''')
    result = db.session.execute(sql, {"sets":sets, "weight":weight, "exercisename":exercisename }).fetchone()
    result=result[0]
    sql    =text('''INSERT INTO visits (time, user_id, exercise_id) VALUES (:time, :user_id, :exercise_id) RETURNING id''')
    result = db.session.execute(sql, {"time":time, "user_id":user_id, "exercise_id":result}).fetchone()
    db.session.commit()
    visit_id = result[0]
    if request.form["Continue"] == "True":
        return render_template("form.html", exercises=exercisename)
    else:
        return render_template("index.html", added=True)

@app.route("/profile/<int:id>")
def profile(id):
    #first we get the visit id.
    #sql = text("SELECT v.id, v.time, v.exercise_id")
    sql = text("SELECT exercise.id, exercise.sets  FROM exercise, users, visits WHERE exercise.id=visits.exercise_id")
    exercises= db.session.execute(sql,{"exercise.id":id}).fetchall()
    print(exercises)
    return render_template("profile.html")
    
def find_user_id(username):
    try:
        sql    = text('''SELECT id FROM users WHERE username = :username''')
        user_id= db.session.execute(sql, {"username":username}).fetchone()
        return user_id[0]
    except:
        return