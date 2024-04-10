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

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


 
@app.route("/")
def index():
    
    return render_template("index.html",error= False)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("index.html", error =True)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return render_template("index.html",error=False)
        else:
            return render_template("index.html", error =True)

    return redirect("/")

@app.route("/signin",methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 1:
        return redirect("/")
    if len(password) < 1:
        return redirect("/")
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return redirect("/")
    except:
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/addexercise",methods=["POST"])
def addexercise():
    exercisename = request.form["exercisename"]
    sets   = request.form["sets"]
    weight = request.form["weight"]
    time   = request.form["time"]
    username= session["username"]
    print(username)
    sql    = text('''SELECT id FROM users WHERE username = :username''')
    user_id= db.session.execute(sql, {"username":username}).fetchone()
    user_id= user_id[0]
    sql    = text('''INSERT INTO exercise (sets, weight, user_id, exercisename)
                  VALUES (:sets, :weight, :user_id, :exercisename) RETURNING id''')
    result = db.session.execute(sql, {"sets":sets, "weight":weight,"user_id":user_id, "exercisename":exercisename })
    sql    =text('''INSERT INTO visits (time) VALUES (:time) RETURNING id''')
    result = db.session.execute(sql, {"time":time, "exercise_id":result})
    #sql = text('INSERT INTO visits (exercise, Sets) VALUES (:exercise, :Sets) RETURNING id;')
    #result = db.session.execute(sql, {"exercise":exercisename, "Sets" :Sets})
    db.session.commit()
    visit_id = result.fetchone()[0]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)