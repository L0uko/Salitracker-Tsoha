from db import db
from flask import redirect, render_template, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
def register():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 1:
        return 2
    if len(password) < 1:
        return 3
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return 1
    except:
        return 4
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return "not_user"
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"]  = find_user_id(username)
            return True
        else:
            return False
def find_user_id(username):
    try:
        sql    = text('''SELECT id FROM users WHERE username = :username''')
        user_id= db.session.execute(sql, {"username":username}).fetchone()
        return user_id[0]
    except:
        return
def show_exercises(user_id):
    sql = text("""
    SELECT e.exercisename, e.sets, e.weight, v.date
    FROM exercise e, visits v 
    WHERE v.exercise_id=e.id and v.user_id=:user_id
    ORDER BY v.date
    """)
    all_exercises = db.session.execute(sql,{"user_id":user_id}).fetchall()
    
    sql= text("""
    SELECT c.cardioname, c.lenght, c.times, v.date 
    FROM cardio c, visits v
    WHERE v.cardio_id = c.id and v.user_id=:user_id
    ORDER BY v.date
              """)
    all_cardio = db.session.execute(sql,{"user_id":user_id}).fetchall()
    return all_exercises, all_cardio
def add_gym():
    exercisename = request.form["exercisename"]
    sets   = request.form["sets"]
    weight = request.form["weight"]
    date   = request.form["date"]
    username= session["username"]
    user_id= find_user_id(username)
    sql    = text('''INSERT INTO exercise (sets, weight, exercisename)
                  VALUES (:sets, :weight, :exercisename) RETURNING id''')
    result = db.session.execute(sql, {"sets":sets, "weight":weight, "exercisename":exercisename }).fetchone()
    result=result[0]
    sql    =text('''INSERT INTO visits (date, user_id, exercise_id) VALUES (:date, :user_id, :exercise_id) RETURNING id''')
    result = db.session.execute(sql, {"date":date, "user_id":user_id, "exercise_id":result}).fetchone()
    db.session.commit()
    visit_id = result[0]
    if request.form["Continue"] == "True":
        return exercisename
    else:
        return False
def add_cardio():
    cardioname = request.form["exercisename"]
    lenght  = request.form["Distance"]
    times = request.form["time"]
    date   = request.form["date"]
    username= session["username"]
    user_id= find_user_id(username)
    sql    = text('''INSERT INTO cardio (cardioname, lenght,times)
                  VALUES (:cardioname, :lenght, :times) RETURNING id''')
    result = db.session.execute(sql, {"cardioname":cardioname, "lenght":lenght, "times":times }).fetchone()
    result=result[0]
    sql    =text('''INSERT INTO visits (date, user_id, cardio_id) VALUES (:date, :user_id, :cardio_id) RETURNING id''')
    result = db.session.execute(sql, {"date":date, "user_id":user_id, "cardio_id":result}).fetchone()
    db.session.commit()
    visit_id = result[0]
    if request.form["Continue"] == "True":
        return cardioname
    else:
        return False
    pass    
def new_quote():
    lenght = db.session.execute(text("SELECT quotes FROM quotes;")).fetchall()
    lenght = len(lenght)
    rand = randint(1,lenght)
    quote= db.session.execute(text("SELECT quotes FROM quotes WHERE id=:rand;"),{"rand":rand}).fetchone()
    return quote[0]
def add_quote():
    quote = request.form["quote"]
    if len(quote) >0 and len(quote) < 150:
        user = session["username"]
        quote = f'"{quote} -{user}"'
        sql = text("INSERT INTO quotes (quotes) VALUES (:quotes)")
        result = db.session.execute(sql, {"quotes":quote})
        db.session.commit()
        return True
    else:
        return False
def find_max(id):
    sql = text("""--sql
    SELECT DISTINCT e.exercisename 
    FROM exercise e, visits v, users u
    WHERE v.user_id = :user_id and e.id=v.exercise_id""")
    names = db.session.execute(sql,{"user_id":id}).fetchall()
    max_list = []
    for name in names:
        print("TESTI")
        print(name)
        name= name[0]
        sql = text("""--sql
            SELECT MAX(e.weight) 
            FROM exercise e, visits v, users u
            WHERE v.user_id=:id and e.id=v.exercise_id and e.exercisename=:name
            """)
        max = db.session.execute(sql,{"id":id, "name":name}).fetchone()
        max = max[0]
        max = (name, max)
        max_list.append(max)
    return max_list
#psql -d db-name -U db-username postgres