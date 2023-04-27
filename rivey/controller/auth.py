from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/login')
def login():
    return render_template('auth/login.html')

@views.route('/signup')
def signup():
    return render_template('auth/signup.html')

@views.route('/forgot-password')
def forgotPassword():
    return render_template('auth/forgot-password.html')
