from flask import Blueprint, render_template, url_for, Flask, redirect, request
from flask_login import login_required, current_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
#from website import app, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretdonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/profile')
@login_required
def profile():
    name = current_user
    return render_template('profile.html', name=current_user.name)

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    users = list(User.query.all())
    print(users)
    if request.method == "POST":
        t = request.form['email']
        print(t)
    return render_template('login.html', current_user=current_user)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)

    