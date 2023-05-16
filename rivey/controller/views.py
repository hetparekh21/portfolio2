from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@views.route('/index')
@login_required
def home():
    return render_template('screen/index.html')

@views.route("/messages")
@login_required
def messages():
    return render_template('screen/messages.html')