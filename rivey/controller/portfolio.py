from flask import Blueprint, render_template, request
from rivey import db
from rivey.models import Messages

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/index')
@portfolio.route('/')
@portfolio.route('/home')
def portfolio_page():
    return render_template('portfolio/index.html')

@portfolio.route('/about')
def about_page():
    return render_template('portfolio/about.html')

@portfolio.route('/contact')
def contact_page():
    return render_template('portfolio/contact.html')

@portfolio.route('/portfolio')
def projects_page():
    return render_template('portfolio/portfolio.html')

@portfolio.route('/services')
def services_page():
    return render_template('portfolio/services.html')

# add message to database
@portfolio.route('/add_message', methods=['POST'])
def add_message():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    userId = request.form['userId']

    new_message = Messages(name=name, email=email, subject=subject, message=message, userId=userId)
    db.session.add(new_message)
    db.session.commit()
    return render_template('portfolio/contact.html', message_sent=True)
