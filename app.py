import re
import os
from flask import Flask, request, redirect, render_template, session

from database import sql_fetch, sql_fetch_one, sql_write
from models import menu, user, reviews

import bcrypt

SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template('index.jinja')

@app.route('/menu')
def index():
    name = user.get_user_name()
    food_items = menu.get_all_food()
    user_reviews = reviews.get_all()
    print(user_reviews)
    return render_template('menu.jinja', food_items=food_items, name=name, user_reviews=user_reviews)

@app.route('/show_food')
def show():
    name = user.get_user_name()
    item_id = request.args.get('id')
    food_item = menu.get_food_item(item_id)

    print(food_item)
    
    return render_template('show.jinja', food_item = food_item, name=name)

@app.route('/add_food')
def add():
  name = user.get_user_name()
  if name:
    return render_template('add_food.jinja', name=name)
  else: 
    return redirect('/login')


@app.route('/add_food', methods=["POST"])
def addpost():
  if user.get_user_name():
    name = request.form.get('name')
    price = float(re.findall('\d+', request.form.get('price'))[0])    
    image_url = request.form.get('image_url')

    menu.insert_food(name, price, image_url)

  return redirect('/menu')

@app.route('/edit_food')
def update():
    name = user.get_user_name()
    if name:
      item_id = request.args.get('id')
      food_item = menu.get_food_item(item_id)
      return render_template("edit_food.jinja", food_item = food_item, name=name)
    else:
      return render_template("login.jinja")

@app.route('/edit_food', methods=["POST"])
def editpost():
    if user.get_user_name():
      item_id = request.args.get('id')
      name = request.form.get('name')
      image_url = request.form.get('image_url')
      price = float(re.findall('\d+', request.form.get('price'))[0])

      menu.update_food(item_id, name, image_url, price)

      return redirect(f'/show_food?id={item_id}')
    else:
      return redirect('/login')

@app.route('/delete_food', methods=["GET","POST"])
def delete():
  if user.get_user_name():
    item_id = request.args.get('id')
    menu.delete_food(item_id)

  return redirect('/menu')
  
@app.route('/add_review', methods=["POST"])
def add_review():
  if user.get_user_name:
    user_id = session['user_id']
    content = request.form.get('review')
    reviews.add(user_id, content)
    return redirect('/menu')
  else:
    return redirect('/login')

@app.route('/signup')
def signup_form():
  return render_template('signup.jinja')

@app.route('/signup', methods=['POST'])
def signup_action():
  email = request.form.get('email')
  name = request.form.get('name')
  password = request.form.get('password')
  print(password)
  pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)", [email, name, pw_hash])
  return redirect('/login')


@app.route('/login')
def login():
    return render_template("login.jinja")

@app.route('/login', methods=["POST"])
def loginpost():
    email = request.form.get('email')
    password = request.form.get('password')

    current_user = user.get_user(email)
    if current_user:
      password_hash = current_user[3]
      valid = bcrypt.checkpw(password.encode(), password_hash.encode())

    if current_user and valid:
      session['user_id'] = current_user[0]
      session['user_email'] = current_user[1]
      session['username'] = current_user[2]
      return redirect('/menu')
    elif not current_user:
      print('user does not exist')
      return redirect('/login')
    elif not valid:
      print('password incorrect')
      return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/menu')


app.run(debug=True)