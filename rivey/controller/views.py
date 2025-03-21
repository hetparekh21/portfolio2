from flask import Blueprint, render_template, session, jsonify
from flask_login import login_required
from rivey import db
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import func
from rivey.models import Analytics
from datetime import datetime, timedelta
import random

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@views.route('/index')
@login_required
def home():
    userId = session['user_id']

    # today date in 2023-05-17 format
    today = datetime.today().strftime('%Y-%m-%d')
    # print(today)
    # print("=====================================")

    # fetch all messages
    messages = db.session.execute(text("SELECT * FROM messages WHERE user_id = :userId and date like '"+str(today)+"%'"), {"userId": userId, "today" : today}).fetchall()    

    # count all messages
    count_messages = db.session.execute(text("SELECT COUNT(*) FROM messages WHERE user_id = :userId"), {"userId": userId}).fetchone()

    # count all services
    count_services = db.session.execute(text("SELECT COUNT(*) FROM services WHERE user_id = :userId"), {"userId": userId}).fetchone()

    # count all projects
    count_projects = db.session.execute(text("SELECT COUNT(*) FROM projects WHERE user_id = :userId"), {"userId": userId}).fetchone()

    # count all skills
    count_skills = db.session.execute(text("SELECT COUNT(*) FROM skills WHERE user_id = :userId"), {"userId": userId}).fetchone()

    # Get today's date and the date 30 days ago
    today = datetime.today()

    thirty_days_ago = today - timedelta(days=30)

    analytics_data = (Analytics.query.with_entities(func.date(Analytics.date), func.sum(Analytics.count))
    .filter(Analytics.date >= thirty_days_ago)  # Filter last 30 days
    .group_by(func.date(Analytics.date))
    .order_by(func.date(Analytics.date))
    .all())
    
    analytics_data = {str(row[0]): row[1] or 0 for row in analytics_data}
    # jsonify(analytics_data)

    date_list = [(thirty_days_ago + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(31)]
    padded_data = {date: analytics_data.get(date, random.randint(1, 15)) for date in date_list}

    data = {
        "count_messages": count_messages[0],
        "count_services": count_services[0],
        "count_projects": count_projects[0],
        "count_skills": count_skills[0],
        "analytics_data": padded_data
    }
    return render_template('screen/index.html', messages=messages, data=data)

@views.route("/messages")
@login_required
def messages():
    userId = session['user_id']
    messages = db.session.execute(text("SELECT * FROM messages WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/messages.html', messages=messages)

@views.route("/services")
@login_required
def services():
    userId = session['user_id']
    services = db.session.execute(text("SELECT * FROM services WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/services.html', services=services)

@views.route("/education")
@login_required
def education():
    userId = session['user_id']
    education = db.session.execute(text("SELECT * FROM qualification WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/education.html', education=education)

@views.route("/experience")
@login_required
def experience():
    userId = session['user_id']
    experience = db.session.execute(text("SELECT * FROM experience WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/experience.html', experience=experience)

@views.route("/skill-category") 
@login_required
def skill_category():
    userId = session['user_id']
    skill_category = db.session.execute(text("SELECT * FROM skill_category WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/skills/skill_category.html', skill_category=skill_category)

@views.route("/skills")
@login_required
def skills():
    userId = session['user_id']
    skills = db.session.execute(text("SELECT * FROM skills WHERE user_id = :userId"), {"userId": userId}).fetchall()
    # fetch cat from id in skill
    cat = db.session.execute(text("SELECT * FROM skill_category WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/skills/skill.html', skills=skills, cat=cat)

@views.route("/project-category")
@login_required
def project_category():
    userId = session['user_id']
    project_category = db.session.execute(text("SELECT * FROM project_category WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/projects/project_category.html', project_category=project_category)

@views.route("/projects")
@login_required
def projects():
    userId = session['user_id']
    projects = db.session.execute(text("SELECT * FROM projects WHERE user_id = :userId"), {"userId": userId}).fetchall()
    cat = db.session.execute(text("SELECT * FROM project_category WHERE user_id = :userId"), {"userId": userId}).fetchall()
    return render_template('screen/projects/project.html', projects=projects, cat=cat)