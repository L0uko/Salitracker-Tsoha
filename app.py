from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Heipparallaa!. Tämä on testi. "

@app.route("/new1")
def index():
    return "Heipparallaa!. Tämä on testi. "
