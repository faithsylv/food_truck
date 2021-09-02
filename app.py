from database import sql_fetch, sql_write
import re
from flask import Flask, request, redirect, render_template, session
import psycopg2
import os

app = Flask(__name__)

dbname = 'foodtruck'

def get_user_name():
  if 'user_id' in session:
    user_id = session['user_id']
    results = sql_fetch('SELECT name FROM users WHERE id = %s', [user_id])
    name = results[0][0]
    return name
  return ''

@app.route('/')
def home():
    return render_template('index.jinja')

@app.route('/menu')
def index():
    conn = psycopg2.connect(f"dbname={dbname}")
    cur = conn.cursor()
    cur.execute("SELECT * from food")
    results = cur.fetchall()
    print(f'the results are {results}')
    food_items = []
    for row in results:
        food_item = {
            'id': row[0],
            'name': row[1],
            'image': row[2],
            'price': f'${float(row[3]):.2f}',
        }
        food_items.append(food_item)
    cur.close()
    conn.close()
    return render_template('menu.jinja', food_items=food_items)

@app.route('/show_food')
def show():
    conn = psycopg2.connect(f"dbname={dbname}")
    cur = conn.cursor()

    item_id = request.args.get('id')
    cur.execute("SELECT * FROM food WHERE id=%s", [item_id])
    results = cur.fetchone()
    
    food_item = {
        'id': results[0],
        'name': results[1],
        'image': results[2],
        'price': f'${float(results[3]):.2f}'
    }

    print(food_item['image'])

    cur.close()
    conn.close()

    return render_template('show.jinja', food_item = food_item)

@app.route('/add_food')
def add():
    return render_template('add_food.jinja')

@app.route('/add_food', methods=["POST"])
def addpost():
  # Inspect the request data
  print(request.form)

  conn = psycopg2.connect(f"dbname={dbname}")
  cur = conn.cursor()
  name = request.form.get('name')
  # Will have to convert price to whatever format you chose for the DB
  price = float(request.form.get('price'))
  image_url = request.form.get('image_url')
  cur.execute("INSERT INTO food(name, image_url, price) VALUES (%s, %s, %s)", [name, image_url, price])
  conn.commit() # Don't forget this, or it won't save.
  cur.close()
  conn.close()
  # Show without redirect first
  return redirect('/menu')

@app.route('/edit_food')
def update():
    conn = psycopg2.connect(f"dbname={dbname}")
    cur = conn.cursor()

    item_id = request.args.get('id')
    cur.execute("SELECT * FROM food WHERE id=%s", [item_id])
    results = cur.fetchone()
    
    food_item = {
        'id': results[0],
        'name': results[1],
        'image': results[2],
        'price': f'${float(results[3]):.2f}'
    }

    print(food_item['image'])

    cur.close()
    conn.close()
    return render_template("edit_food.jinja", food_item = food_item)

@app.route('/edit_food', methods=["POST"])
def editpost():
    conn = psycopg2.connect(f"dbname={dbname}")
    cur = conn.cursor()
    item_id = request.args.get('id')
    print('okay the id is', item_id)
    name = request.form.get('name')
    price = float(request.form.get('price'))
    image_url = request.form.get('image_url')
    cur.execute("UPDATE food SET name=%s, image_url=%s, price=%s WHERE id=%s", [name, image_url, price, item_id])
    conn.commit() # Don't forget this, or it won't save.
    cur.close()
    conn.close()
    # Show without redirect first
    return redirect(f'/show_food?id={item_id}')

@app.route('/signup')
def signup_form():
  return render_template('signup.jinja', user_name=get_user_name())

@app.route('/signup', methods=['POST'])
def signup_action():
  email = request.form.get('email')
  name = request.form.get('name')
  sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)", [email, name, pw_hash])
  return redirect('/')


@app.route('/login')
def login():
    return render_template("login.jinja")

@app.route('/login', methods=["POST"])
def login():



    return redirect("/")


# if __name__ == 'main':
app.run(debug=True)