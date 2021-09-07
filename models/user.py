from database import sql_fetch, sql_fetch_one, sql_write
from flask import session 

def get_user(email):
    user = sql_fetch_one("SELECT * FROM users WHERE email = %s", [email])
    return user


def get_user_name():
  if 'user_id' in session:
    name = session['username']
    return name
  return ''


