from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@views.route('/index')
def home():
    return render_template('screen/index.html')

@views.route("/messages")
def messages():
    return render_template('screen/messages.html')