DROP TABLE IF EXISTS food;

CREATE TABLE food (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  image_url VARCHAR(200),
  price INTEGER NOT NULL
);

INSERT INTO food(name, image_url, price) VALUES('Beef Burger', '/static/images/burger.jpg', 1500);
INSERT INTO food(name, image_url, price) VALUES('Veggie Burger', '/static/images/veggeburger.jpg', 1500);
INSERT INTO food(name, image_url, price) VALUES('Fries', '/static/images/fries.jpg', 450);