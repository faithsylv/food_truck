from database import sql_fetch, sql_fetch_one, sql_write

def get_all_food():
    results = sql_fetch("SELECT * from food")
    food_items = []

    for row in results:
        food_item = {
            'id': row[0],
            'name': row[1],
            'image': row[2],
            'price': f'${float(row[3]):.2f}',
        }

        food_items.append(food_item)

    return food_items

def get_food_item(item_id):
    results = sql_fetch_one("SELECT * FROM food WHERE id=%s", [item_id])
    food_item = {
        'id': results[0],
        'name': results[1],
        'image': results[2],
        'price': f'${float(results[3]):.2f}'
    }

    return food_item

def insert_food(name, price, image_url):
    sql_write("INSERT INTO food(name, image_url, price) VALUES (%s, %s, %s)", [name, image_url, price])


def update_food(item_id, name, image_url, price):
    sql_write("UPDATE food SET name=%s, image_url=%s, price=%s WHERE id=%s", [name, image_url, price, item_id])

def delete_food(item_id):
    sql_write("DELETE FROM food WHERE id=%s", [item_id])