from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    service_title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True, default='default-service.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(255), nullable=False)
    field = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.String(255), nullable=False)
    end_date = db.Column(db.String(255), nullable=True)
    is_current = db.Column(db.Boolean, nullable=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.String(255), nullable=False)
    end_date = db.Column(db.String(255), nullable=True)
    is_current = db.Column(db.Boolean, nullable=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.String(255), nullable=True)
    lng = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ProjectCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    client = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True, default='default-project.png')
    category_id = db.Column(db.Integer, db.ForeignKey('project_category.id', ), nullable=False,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SkillCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    

class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    about_title = db.Column(db.String(255), nullable=False)
    about_me = db.Column(db.Text, nullable=False)
    position = db.Column(db.String(255), nullable=False)
    resume = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(255), nullable=True, default='default-profile.png')
    profile_image = db.Column(db.String(255), nullable=True, default='default-profile.png')
    age = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class WebsiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    web_title = db.Column(db.String(255), nullable=False)
    seo = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    favicon = db.Column(db.String(255), nullable=True, default='default-favicon.png')
    logo = db.Column(db.String(255), nullable=True, default='default-logo.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    github = db.Column(db.String(255), nullable=True)
    behance = db.Column(db.String(255), nullable=True)
    dribble = db.Column(db.String(255), nullable=True)
    pinterest = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.String(255), nullable=True)
    stackoverflow = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# table for storing portfolio analytics
class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    count = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 