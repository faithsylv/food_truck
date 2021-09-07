from database import sql_fetch, sql_fetch_one, sql_write

def get_all():
    results = sql_fetch('SELECT reviews.id, content, rating, name FROM reviews INNER JOIN users ON users.id = reviews.user_id')
    reviews = []
    print(results)
    for row in results:

        review = {
            'id': row[0], 
            'content': row[1],
            'rating': row[2],
            'user_name': row[3]
        }

        reviews.append(review)

    return reviews

def add(user_id, content):
    sql_write('INSERT INTO reviews(user_id, content) VALUES (%s, %s)', [user_id, content])
