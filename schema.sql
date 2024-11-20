CREATE TABLE users(id SERIAL PRIMARY KEY, name TEXT, password TEXT);
CREATE TABLE restaurants(id SERIAL PRIMARY KEY, name TEXT UNIQUE, info TEXT, stars_average REAL, created_at TIMESTAMP);
CREATE TABLE reviews(restaurant_id INTEGER, user_id INTEGER, comment TEXT, stars INTEGER, made_at TIMESTAMP);
CREATE TABLE groups(id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE group_restaurants(group_id INTEGER, restaurant_id INTEGER);
