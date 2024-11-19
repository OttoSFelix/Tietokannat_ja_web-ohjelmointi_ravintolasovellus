CREATE TABLE users(id SERIAL PRIMARY KEY, name TEXT UNIQUE, password TEXT);
CREATE TABLE restaurants(id SERIAL PRIMARY KEY, name TEXT UNIQUE, info TEXT, stars_average REAL);
CREATE TABLE reviews(restaurant_id INTEGER REFERENCES restaurants.id, comment TEXT, stars INTEGER);
CREATE TABLE groups(id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE group_restaurants(group_id INTEGER REFERENCES groups.id, restaurant_id INTEGER REFERENCES restaurants.id);
