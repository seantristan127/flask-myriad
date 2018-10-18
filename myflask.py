import os
import sqlite3
import urllib
from urllib.request import urlopen
from flask import Flask, render_template, request, flash, jsonify, url_for
import json


from flask_uploads import UploadSet, IMAGES

from flask_bcrypt import Bcrypt
from werkzeug.utils import redirect

photos = UploadSet('photos', IMAGES)

app = Flask(__name__)

DATABASE = "./myriad.db"

app.config['SECRET_KEY'] = '290d63efdb9e78f5a7824aef129fe7c6'

bcrypt = Bcrypt()

if not os.path.exists(DATABASE):
    print("DATABASE HAS BEEN CREATED")
    db_conn = sqlite3.connect('myriad.db')

    cursor = db_conn.cursor()

    try:
        cursor.execute('''CREATE TABLE user(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        user_fname VARCHAR(45) NOT NULL,
                        user_lname VARCHAR(45) NOT NULL,
                        user_email VARCHAR(45) NOT NULL,
                        user_password VARCHAR(45) NOT NULL,
                        user_isActive BOOLEAN NOT NULL,
                        user_isAdmin BOOLEAN NOT NULL
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE genre(
                        genre_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        genre_name VARCHAR(45) NOT NULL
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE type(
                        type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        type_name VARCHAR(45) NOT NULL
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE comment(
                        comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        comment_text TEXT NOT NULL,
                        user_id VARCHAR(45) NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES user(user_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE rating(
                        rating_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        rating_score FLOAT,
                        user_id VARCHAR(45) NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES user(user_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book(
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        book_name VARCHAR(45) NOT NULL,
                        book_description VARCHAR(45) NOT NULL,
                        book_author VARCHAR(45) NOT NULL,
                        book_picture VARCHAR(45),
                        book_isbn VARCHAR(45) NOT NULL,
                        book_average_rating FLOAT,
                        type_id VARCHAR(45) NOT NULL,
                        FOREIGN KEY(type_id) REFERENCES type(type_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book_comment(
                        comment_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        FOREIGN KEY(comment_id) REFERENCES comment(comment_id),
                        FOREIGN KEY(book_id) REFERENCES book(book_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book_rating(
                        rating_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        FOREIGN KEY(rating_id) REFERENCES rating(rating_id),
                        FOREIGN KEY(book_id) REFERENCES book(book_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book_genre(
                        genre_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        FOREIGN KEY(genre_id) REFERENCES genre(genre_id),
                        FOREIGN KEY(book_id) REFERENCES book(book_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE user_library(
                        user_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES user(user_id),
                        FOREIGN KEY(book_id) REFERENCES book(book_id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    db_conn.close()

else:
    print("DATABASE ALREADY EXIST")


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html', title = 'Sign Up')


@app.route("/admin_signin")
def admin_signin():
    return render_template('admin_signin.html', title = 'Sign In as Administrator')


@app.route("/signin")
def signin():
    return render_template('signin.html', title = 'Sign In')


@app.route("/login_user", methods=['GET', 'POST'])
def login_user():

    if request.method == 'POST':
        email_address = request.form['email']
        password = request.form['password']

        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute("SELECT user_email FROM user WHERE user_email = ?", (email_address,))
        email_check = cursor.fetchone()

        cursor.execute("SELECT user_password FROM user WHERE user_email = ?", (email_address,))
        hashed_pw = cursor.fetchone()

        try:
            if bcrypt.check_password_hash(hashed_pw[0], password) and email_address == email_check[0]:

                cursor.execute("SELECT user_isAdmin FROM user WHERE user_email = ?", (email_address,))
                is_admin = cursor.fetchone()

                cursor.execute("SELECT user_lname FROM user WHERE user_email = ?", (email_address,))
                user_name = cursor.fetchone()

                response = urllib.request.urlopen('http://127.0.0.1:5000/users_api').read()

                jsonResponse = json.loads(response)


                db_conn.commit()
                db_conn.close()

                if is_admin[0]:
                    print("Im admin")
                    return redirect(url_for('admin'))
                else:
                    print("Im user")
                    return redirect(url_for('user', name = user_name[0]))
            else:
                flash("Invalid input")
        except TypeError as e:
            pass

    return render_template('index.html')


@app.route("/admin_form", methods=['GET', 'POST'])
def admin_form():

    if request.method == 'POST':

        email_address = request.form['email']
        password = request.form['password']

        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute("SELECT user_email FROM user WHERE user_email = ?", (email_address,))
        email_check = cursor.fetchone()

        cursor.execute("SELECT user_password FROM user WHERE user_email = ?", (email_address,))
        hashed_pw = cursor.fetchone()

        try:
            if bcrypt.check_password_hash(hashed_pw[0], password) and email_address == email_check[0]:

                cursor.execute("SELECT user_isAdmin FROM user WHERE user_email = ?", (email_address,))
                is_admin = cursor.fetchone()

                cursor.execute("SELECT user_lname FROM user WHERE user_email = ?", (email_address,))
                user_name = cursor.fetchone()

                db_conn.commit()
                db_conn.close()

                print(is_admin[0])
                if is_admin[0]:
                    return render_template('dashboard.html')
                else:
                    return "<script>alert('Permission Denied')</script>"
            else:
                flash("Invalid input")
        except TypeError as e:
            pass

    return render_template('index.html')


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    return render_template('add_user.html')


@app.route("/process_user", methods=['GET', 'POST'])
def process_user():
    print("in")
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['pass']

        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')
        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute("SELECT COUNT(user_email), * FROM user WHERE user_email = ?", (email,))
        count = cursor.fetchone()

        if len(count) <= 0:
            cursor.execute("INSERT INTO user(user_fname, user_lname, user_email, user_password, user_isActive, user_isAdmin) VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, email, hashed_pw, True, False))
        else:
            return "Error"
        db_conn.commit()

        db_conn.close()

    return render_template('index.html')


@app.route("/admin_add_user", methods=['POST'])
def admin_add_user():
    print("hello")
    if request.method == 'POST':

        print("hello")
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']

        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')
        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute(
            "INSERT INTO user(user_fname, user_lname, user_email, user_password, user_isActive, user_isAdmin) VALUES (?, ?, ?, ?, ?, ?)",
            (first_name, last_name, email, hashed_pw, True, False))

        db_conn.commit()

        db_conn.close()

    '''return jsonify({
        'username' : user_name,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
    })'''
    return "<script>alert('Book Successfully Added!')</script>"


@app.route("/admin")
def admin():
    return render_template('admin.html')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/all_books")
def all_books():

    db_conn = sqlite3.connect('myriad.db')

    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()

    cursor.execute("SELECT COUNT(distinct book_comment.book_id) FROM book_comment INNER JOIN book ON book_comment.book_id = book.book_id")
    comment = cursor.fetchall()

    return render_template('all_books.html', books = books, comment = comment)


@app.route("/all_user")
def all_user():

    db_conn = sqlite3.connect('myriad.db')

    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM user")
    user = cursor.fetchall()
    return render_template('all_user.html', users = user)


@app.route("/upload_book", methods=['GET', 'POST'])
def upload_book():
    print("hello")
    if request.method == 'POST':
        name = request.form['book_name']
        print(name)
        description = request.form['description']
        author = request.form['author']
        image = "x"
        isbn = request.form['isbn']
        type = '1'
        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute(
            "INSERT INTO book(book_name, book_description, book_author, book_isbn, book_average_rating, book_picture) VALUES (?, ?, ?, ?, ?, ?)",
            (name, description, author, isbn, 0, image))

        db_conn.commit()
        db_conn.close()

    return "<script>alert('Book Successfully Added!')</script>"


@app.route("/add_books")
def add_books():
    return render_template('add_books.html')


@app.route("/logout")
def logout():
    return render_template('logout.html')


@app.route("/user")
def user():
    return render_template('user.html')


@app.route("/library")
def library():
    return render_template('/library.html')


@app.route("/save_book", methods=['GET', 'POST'])
def save_book():
    print("hello")
    if request.method == 'POST':

        book_id = request.form['id']
        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute("INSERT INTO user_library(user_id, book_id) VALUES (?, ?)", (1, book_id))

        db_conn.commit()
        db_conn.close()

    return "<script>alert('Book Successfully Added!')</script>"

def dict_factory(cursor, row):
    d = {}
    
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/users_api")
def admin_api():

    db_conn = sqlite3.connect('myriad.db')
    db_conn.row_factory = dict_factory

    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()
    db_conn.close()

    return jsonify(results)


@app.route("/books_api")
def books_api():

    db_conn = sqlite3.connect('myriad.db')
    db_conn.row_factory = dict_factory

    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM book")
    results = cursor.fetchall()
    db_conn.close()

    return jsonify(results)


@app.route("/browse")
def browse():
    db_conn = sqlite3.connect('myriad.db')

    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()

    cursor.execute("SELECT COUNT(distinct book_comment.book_id) FROM book_comment INNER JOIN book ON book_comment.book_id = book.book_id")
    comment = cursor.fetchall()

    return render_template('browse.html', books=books, comment=comment)


if __name__ == "__main__":
    app.run(debug = True)
