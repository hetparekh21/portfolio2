from flask import Blueprint, render_template, request, redirect, url_for, flash
from rivey import db
from rivey.models import *

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/index/<id>')
@portfolio.route('/<id>')
@portfolio.route('/home/<id>')
def portfolio_page(id):
    userId = id

    # fetch data from about
    about = About.query.filter_by(user_id=int(userId)).first()
    social = Social.query.filter_by(user_id=int(userId)).first()
    contact = Contact.query.filter_by(user_id=int(userId)).first()
    website = WebsiteSetting.query.filter_by(user_id=int(userId)).first()

    return render_template('portfolio/index.html', about=about, social=social, contact=contact, userId=userId, website=website)

@portfolio.route('/about/<id>')
def about_page(id):
    userId = id
    about = About.query.filter_by(user_id=int(userId)).first()
    if about is None:
        about = {'profile_image' : '', 'image' : ''}
    skills = Skills.query.filter_by(user_id=int(userId)).all()
    education = Qualification.query.filter_by(user_id=int(userId)).all()
    experience = Experience.query.filter_by(user_id=int(userId)).all()
    contact = Contact.query.filter_by(user_id=int(userId)).first()
    website = WebsiteSetting.query.filter_by(user_id=int(userId)).first()

    # sort education by start_date
    education.sort(key=lambda x: x.start_date, reverse=True)
    experience.sort(key=lambda x: x.start_date, reverse=True)

    return render_template('portfolio/about.html', about=about, skills=skills, education=education, experience=experience, contact=contact, userId=userId, website=website)

@portfolio.route('/contact/<id>')
def contact_page(id):
    userId = id
    contact = Contact.query.filter_by(user_id=int(userId)).first()
    website = WebsiteSetting.query.filter_by(user_id=int(userId)).first()
    return render_template('portfolio/contact.html', contact=contact, userId=userId, website=website)

@portfolio.route('/portfolio/<id>')
def projects_page(id):
    userId = id
    projects = Projects.query.filter_by(user_id=int(userId)).all()
    category = ProjectCategory.query.filter_by(user_id=int(userId)).all()
    website = WebsiteSetting.query.filter_by(user_id=int(userId)).first()
    return render_template('portfolio/portfolio.html', projects=projects, category=category, userId=userId, website=website)

@portfolio.route('/services/<id>')
def services_page(id):
    userId = id

    # fetch services from database
    services = Services.query.filter_by(user_id=int(userId)).all()
    website = WebsiteSetting.query.filter_by(user_id=int(userId)).first()

    return render_template('portfolio/services.html', services=services, userId=userId, website=website)

# add message to database
@portfolio.route('/send-message', methods=['POST'])
def add_message():
    userId = request.form['id']
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    try:
        new_message = Messages(name=name, email=email, subject=subject, message=message, user_id=userId)
        db.session.add(new_message)
        db.session.commit()

        flash('Message sent successfully',category='success')
    except Exception as e:
        print('Error adding message to database')
        

    return redirect(url_for('portfolio.contact_page', id=userId))
    
