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
TODO See profile
TODO profile sort by time exercises
TODO Running
TODO route where can choose between running and gym 
(maybe 3rd option? sport?)
TODO
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
    return redirect("/")


@app.route("/form")
def form():
    try:
        if len(session["username"]) < 0:
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
    sql    = text('''INSERT INTO exercise (sets, weight, user_id, exercisename)
                  VALUES (:sets, :weight, :user_id, :exercisename) RETURNING id''')
    result = db.session.execute(sql, {"sets":sets, "weight":weight,"user_id":user_id, "exercisename":exercisename })
    sql    =text('''INSERT INTO visits (time) VALUES (:time) RETURNING id''')
    result = db.session.execute(sql, {"time":time, "exercise_id":result})
    #sql = text('INSERT INTO visits (exercise, Sets) VALUES (:exercise, :Sets) RETURNING id;')
    #result = db.session.execute(sql, {"exercise":exercisename, "Sets" :Sets})
    db.session.commit()
    visit_id = result.fetchone()[0]
    return render_template("index.html",exerciseadd = True)

@app.route("/profile/<int:id>")
def profile(id):
    #id = find_user_id(session["username"])
    return render_template("profile.html")
    #allow=False
    #if is_admin():
    #    allow = True
    #elif is_user() and user_id() == id:
    #    allow = True
    #
    #if not allow:
    #    return render_template("index.html", error="Ei oikeutta nähdä sivua")
    
def find_user_id(username):
    try:
        sql    = text('''SELECT id FROM users WHERE username = :username''')
        user_id= db.session.execute(sql, {"username":username}).fetchone()
        return user_id[0]
    except:
        return