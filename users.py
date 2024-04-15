from db import db
from flask import redirect, render_template, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

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

def find_user_id(username):
    try:
        sql    = text('''SELECT id FROM users WHERE username = :username''')
        user_id= db.session.execute(sql, {"username":username}).fetchone()
        return user_id[0]
    except:
        return