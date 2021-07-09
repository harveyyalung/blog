from flask import Blueprint, render_template, url_for, Flask, redirect, request
from flask_login import login_required, current_user, UserMixin, LoginManager, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, email_validator, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
#from website import app, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretdonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
Bootstrap(app)
db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))

class LoginForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exist. Please choose a different one.")
########################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

########################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    name = current_user
    login.user = form
    return render_template('profile.html', name=current_user.name, form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login.user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>' + form.username.data + '' + form.password.data + '</h1>'

    return render_template('login.html', current_user=current_user, form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "<h1>New user has been created!</h1>"
        #return '<h1>' + form.username.data + '' + form.email.data + '' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)


