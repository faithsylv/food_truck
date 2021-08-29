import psycopg2
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.jinja')

@app.route('/menu')
def index():
    conn = psycopg2.connect("dbname=food_truck")
    cur = conn.cursor()
    cur.execute("SELECT * from food")
    results = cur.fetchall()
    print('the results are', results)
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

@app.route('/add_food')
def add():
    return render_template('add_food.jinja')

@app.route('/add_food', methods=["POST"])
def addpost():
  # Inspect the request data
  print(request.form)

  conn = psycopg2.connect("dbname=food_truck")
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

if __name__ == 'main':
    app.run(debug=True)