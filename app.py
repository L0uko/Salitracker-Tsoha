from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
#How to make new image and run server:
#docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])
