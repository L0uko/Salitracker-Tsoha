from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
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
    Sets   = request.form["Sets"]
    weight = request.form["Weight"]
    Time   = request.form["Time"]
    sql    = text('INSERT INTO ')
    sql = text('INSERT INTO visits (exercise, Sets) VALUES (:exercise, :Sets) RETURNING id;')
    result = db.session.execute(sql, {"exercise":exercisename, "Sets" :Sets})
    db.session.commit()
    poll_id = result.fetchone()[0]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)