from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from time import sleep

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return redirect('/etusivu')

@app.route('/etusivu')
def etusivu():
    sql = "SELECT id, name, created_at, stars_average FROM restaurants ORDER BY id DESC"
    result = db.session.execute(text(sql))
    restaurants = result.fetchall()
    return render_template("etusivu.html", restaurants=restaurants)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["nimi"]
    info = request.form["info"]
    sql = "INSERT INTO restaurants (name, info, created_at) VALUES (:name, :info, NOW()) RETURNING id"
    result = db.session.execute(text(sql), {"name":name, 'info':info})
    restaurant_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/etusivu")

@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT info FROM restaurants WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    info = result.fetchone()
    sql = "SELECT r.id, r.comment, r.made_at, r.stars, u.name FROM reviews r, users u WHERE u.id = r.user_id AND r.restaurant_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    reviews = result.fetchall()
    return render_template("restaurant.html", id=id, name=name, info=info[0], reviews=reviews)

@app.route('/review/<int:id>')
def review(id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    name = result.fetchone()[0]
    return render_template('review.html', id=id, name=name)

@app.route("/maker", methods=["POST"])
def maker():
    lista = []
    review_id = request.form['id']
    teksti = request.form["teksti"]
    stars = request.form["stars"]
    sql = 'SELECT id FROM users WHERE name=:name'
    result = db.session.execute(text(sql), {"name":session['username']})
    user_id = result.fetchone()[0]
    print(f"käyttäjä id = {user_id}")
    sql = "INSERT INTO reviews (restaurant_id, user_id, comment, stars, made_at) VALUES (:id, :user_id, :text, :stars, NOW())"
    db.session.execute(text(sql), {"id":review_id, "user_id":user_id, "text":teksti, "stars":stars})
    db.session.commit()
    sql = "SELECT stars FROM reviews WHERE restaurant_id=:id"
    results = db.session.execute(text(sql), {"id":review_id}).fetchall()
    for result in results:
        lista.append(int(result[0]))
    avg = sum(lista)/len(lista)
    sql = 'UPDATE restaurants SET stars_average = :avg WHERE id = :id'
    db.session.execute(text(sql), {"avg":avg, "id":review_id})
    db.session.commit()
    return redirect("/etusivu")

@app.route('/search', methods=['POST'])
def search():
    search_field = (request.form['search_field']).strip()
    print(f'search field = {search_field}')
    sql = "SELECT id, name, created_at, stars_average FROM restaurants WHERE LOWER(info) LIKE LOWER(:field) OR LOWER(name) LIKE LOWER(:field) ORDER BY id DESC"
    result = db.session.execute(text(sql), {'field': f'%{search_field}%'})
    restaurants = result.fetchall()
    return render_template('search.html', field=search_field, restaurants=restaurants)

@app.route('/ordered')
def ordered():
    sql = "SELECT id, name, created_at, stars_average FROM restaurants ORDER BY stars_average DESC"
    result = db.session.execute(text(sql))
    restaurants = result.fetchall()
    return render_template("ordered.html", restaurants=restaurants)

@app.route('/d_review', methods=['POST'])
def d_review():
    lista = []
    review_id = request.form['rev_id']
    restaurant_id = request.form['res_id']
    sql = 'DELETE FROM reviews WHERE id=:id'
    db.session.execute(text(sql), {'id':review_id})
    db.session.commit()
    print('tähän päästiin')
    sql = "SELECT stars FROM reviews WHERE restaurant_id=:id"
    results = db.session.execute(text(sql), {"id":restaurant_id}).fetchall()
    for result in results:
        lista.append(int(result[0]))
    avg = sum(lista)/len(lista)
    sql = 'UPDATE restaurants SET stars_average = :avg WHERE id = :id'
    db.session.execute(text(sql), {"avg":avg, "id":restaurant_id})
    db.session.commit()
    return redirect('/etusivu')


@app.route('/invalid')
def invalid():
    return render_template('invalid.html')



@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hash_pass = generate_password_hash(password)
    sql = "SELECT id, password FROM users WHERE name=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        sql = 'INSERT INTO users (name, password) VALUES (:name, :password)'
        db.session.execute(text(sql), {'name':username, 'password':hash_pass})
        db.session.commit()
        session["username"] = username
        return redirect("/etusivu")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/etusivu")
        else:
            return redirect('/invalid')

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")