import os
import sqlite3
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt

app = Flask(__name__)

DATABASE = "./myriad.db"

app.config['SECRET_KEY'] = '290d63efdb9e78f5a7824aef129fe7c6'

bcrypt = Bcrypt()

if not os.path.exists(DATABASE):
    print("DATABASE HAS BEEN CREATED")
    db_conn = sqlite3.connect('myriad.db')

    cursor = db_conn.cursor()

    try:
        cursor.execute('''CREATE TABLE users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        user_name VARCHAR(20) NOT NULL,
                        first_name VARCHAR(25) NOT NULL,
                        last_name VARCHAR(25) NOT NULL,
                        email_address VARCHAR(30) NOT NULL,
                        password VARCHAR(20) NOT NULL,
                        account_status BOOLEAN,
                        is_admin BOOLEAN
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE books(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        user_id INTEGER NOT NULL,
                        name VARCHAR(30) NOT NULL,
                        description TEXT NOT NULL,
                        genre VARCHAR NOT NULL,
                        author VARCHAR(40) NOT NULL,
                        ratings FLOAT,
                        picture BLOB,
                        date_time DATETIME NOT NULL,
                        status BOOLEAN NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book_comments(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        book_id INTEGER NOT NULL,
                        comments TEXT,
                        date_time DATETIME NOT NULL,
                        status BOOLEAN NOT NULL,
                        FOREIGN KEY(book_id) REFERENCES books(id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    try:
        cursor.execute('''CREATE TABLE book_ratings(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        user_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        rate FLOAT,
                        status NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(book_id) REFERENCES book(id)
                        );''')

        db_conn.commit()

    except sqlite3.OperationalError as e:
        print(e)

    db_conn.close()
else:
    print("DATABASE ALREADY EXIST")


@app.route("/")
@app.route("/index ")
def index():
    return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html', title = 'Sign Up')


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

        cursor.execute("SELECT email_address FROM users WHERE email_address = ?", (email_address,))
        email_check = cursor.fetchone()

        cursor.execute("SELECT password FROM users WHERE email_address = ?", (email_address,))
        hashed_pw = cursor.fetchone()

        try:
            if bcrypt.check_password_hash(hashed_pw[0], password) and email_address == email_check[0]:

                cursor.execute("SELECT is_admin FROM users WHERE email_address = ?", (email_address,))
                is_admin = cursor.fetchone()

                cursor.execute("SELECT user_name FROM users WHERE email_address = ?", (email_address,))
                user_name = cursor.fetchone()

                db_conn.commit()
                db_conn.close()

                if is_admin[0]:
                    print("Im admin")
                    return render_template('admin.html')
                else:
                    print("Im user")
                    return render_template('user_home.html', name = user_name[0])
            else:
                flash("Invalid input")
        except TypeError as e:
            print(e)

    return render_template('index.html')


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':

        user_name = request.form['username']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['pass']

        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')
        db_conn = sqlite3.connect('myriad.db')

        cursor = db_conn.cursor()

        cursor.execute("INSERT INTO users(user_name, first_name, last_name, email_address, password, account_status, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_name, first_name, last_name, email, hashed_pw, True, False))

        db_conn.commit()

        db_conn.close()

    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/books")
def books():
    return render_template('books.html')


@app.route("/logout")
def logout():
    return render_template('logout.html')


@app.route("/user_home")
def user_home():
    return render_template('user_home.html')


if __name__ == "__main__":
    app.run(debug = True)