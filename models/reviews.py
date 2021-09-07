from database import sql_fetch, sql_fetch_one, sql_write

def get_all_reviews():
    results = sql_fetch('SELECT * FROM reviews')
    reviews = []
    for row in results:

        review = {
            'id': row[0],
            'user_id': row[1], 
            'content': row[2],
            'rating': row[3],
        }

        reviews.append(review)

    return reviews