from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template(index.html)

@app.route("/new1")
def index():
    return "Heipparallaa!. Tämä on testi. "
