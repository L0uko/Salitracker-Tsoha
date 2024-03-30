from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
#How to make new image and run server:
#docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
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

@app.route("/addexersise",methods=["POST"])
def addexersise():
    Exersise = request.form["Exersise"]
    Sets = request.form["Sets"]
    sql = text('INSERT INTO visits (Exersise, Sets) VALUES (:Exersise, :Sets) RETURNING id;')
    result = db.session.execute(sql, {"Exersise":Exersise, "Sets" :Sets})
    #poll_id = result.fetchone()[0]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)