DROP TABLE IF EXISTS food, reviews;

CREATE TABLE food (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  image_url VARCHAR(200),
  price INTEGER NOT NULL
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  content TEXT, 
  rating INTEGER NOT NULL
);


INSERT INTO food(name, image_url, price) VALUES ('Beef Burger', '/static/images/burger.jpg', 1500);
INSERT INTO food(name, image_url, price) VALUES ('Veggie Burger', '/static/images/veggeburger.jpg', 1500);
INSERT INTO food(name, image_url, price) VALUES ('Fries', '/static/images/fries.jpg', 450);

INSERT INTO reviews(user_id, content, rating) VALUES (1, 'here is the post content', 4);