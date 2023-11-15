from flask import Flask
from flask import redirect, render_template, request
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    # We will retrieve the username and the password from the form
    username = request.form["username"]
    password = request.form["password"]
    admin = False

    # We are checking if the checkbox is checked in the form
    try: 
        if request.form["admin"] != None:
            admin = True
    except:
        pass

    # We will make a secure hash value from the password
    hash_value = generate_password_hash(password)

    # We will insert the values from the form in to the users table
    sql = text("INSERT INTO users (username, password, created_at, admin) VALUES (:username, :password, NOW(), :admin)")
    db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
    db.session.commit()

    # After the user creation, we will redirect the user back to the front page
    return redirect("/")