from db import db
from sqlalchemy import text



def find_user_id(username):
    try:
        sql    = text('''SELECT id FROM users WHERE username = :username''')
        user_id= db.session.execute(sql, {"username":username}).fetchone()
        return user_id[0]
    except:
        return