from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    name = current_user
    return render_template('profile.html', name=current_user.name)

@main.route('/login')
def login():
    return render_template('login')

@main.route('/signup')
def signup():
    return render_template('signup')

@main.route('/base')
def base():
    return render_template('base')


 