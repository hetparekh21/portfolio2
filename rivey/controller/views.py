from flask import Blueprint, render_template, session
from flask_login import login_required
from rivey import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@views.route('/index')
@login_required
def home():
    userId = session['user_id']

    # fetch all messages
    messages = db.session.execute("SELECT * FROM messages WHERE user_id = :userId", {"userId": userId}).fetchall()
    # filter messages by current date
    today_message = []
    for message in messages:
        if message[3] == datetime.now().strftime("%Y-%m-%d"):
            today_message.append(message)

    # count all messages
    count_messages = db.session.execute("SELECT COUNT(*) FROM messages WHERE user_id = :userId", {"userId": userId}).fetchone()

    # count all services
    count_services = db.session.execute("SELECT COUNT(*) FROM services WHERE user_id = :userId", {"userId": userId}).fetchone()

    # count all projects
    count_projects = db.session.execute("SELECT COUNT(*) FROM projects WHERE user_id = :userId", {"userId": userId}).fetchone()

    # count all skills
    count_skills = db.session.execute("SELECT COUNT(*) FROM skills WHERE user_id = :userId", {"userId": userId}).fetchone()

    data = {
        "count_messages": count_messages[0],
        "count_services": count_services[0],
        "count_projects": count_projects[0],
        "count_skills": count_skills[0],
    }
    return render_template('screen/index.html', message=today_message, data=data)

@views.route("/messages")
@login_required
def messages():
    userId = session['user_id']
    messages = db.session.execute("SELECT * FROM messages WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/messages.html', messages=messages)

@views.route("/services")
@login_required
def services():
    userId = session['user_id']
    services = db.session.execute("SELECT * FROM services WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/services.html', services=services)

@views.route("/education")
@login_required
def education():
    userId = session['user_id']
    education = db.session.execute("SELECT * FROM qualification WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/education.html', education=education)

@views.route("/experience")
@login_required
def experience():
    userId = session['user_id']
    experience = db.session.execute("SELECT * FROM experience WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/experience.html', experience=experience)

@views.route("/skill-category") 
@login_required
def skill_category():
    userId = session['user_id']
    skill_category = db.session.execute("SELECT * FROM skill_category WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/skills/skill_category.html', skill_category=skill_category)

@views.route("/skills")
@login_required
def skills():
    userId = session['user_id']
    skills = db.session.execute("SELECT * FROM skills WHERE user_id = :userId", {"userId": userId}).fetchall()
    # fetch cat from id in skill
    cat = db.session.execute("SELECT * FROM skill_category WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/skills/skill.html', skills=skills, cat=cat)

@views.route("/project-category")
@login_required
def project_category():
    userId = session['user_id']
    project_category = db.session.execute("SELECT * FROM project_category WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/projects/project_category.html', project_category=project_category)

@views.route("/projects")
@login_required
def projects():
    userId = session['user_id']
    projects = db.session.execute("SELECT * FROM projects WHERE user_id = :userId", {"userId": userId}).fetchall()
    cat = db.session.execute("SELECT * FROM project_category WHERE user_id = :userId", {"userId": userId}).fetchall()
    return render_template('screen/projects/project.html', projects=projects, cat=cat)