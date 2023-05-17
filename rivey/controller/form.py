from flask import Blueprint, render_template, request, url_for, redirect, session
from rivey.models import *
from rivey import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from rivey.controller import views
from flask_login import login_required


form = Blueprint('form', __name__)


@form.route('/edit-profile')
@login_required
def editProfile():
    about = About.query.filter_by(user_id=session['user_id']).first()
    return render_template('forms/edit-profile.html', about=about)


###
# Add Routes
###
@form.route('/add-education', methods=['GET', 'POST'])
@login_required
def addEducation():
    message = ''
    if request.method == 'POST':
        try:
            userid = session['user_id']
            school = request.form['school']
            field = request.form['field']
            description = request.form['description']
            start_date = request.form['start-date']
            is_current = False
            try:
                is_current = request.form['current-study']
                if is_current == 'on':
                    is_current = True

                    education = Qualification(school=school, field=field, description=description,
                                              start_date=start_date, is_current=is_current, user_id=userid)
            except:
                end_date = request.form['end-date']
                is_current = False

                education = Qualification(school=school, field=field, description=description,
                                          start_date=start_date, end_date=end_date, is_current=is_current, user_id=userid)

            db.session.add(education)
            db.session.commit()

            message = {
                'status': 'success',
                'message': 'Qualification added successfully'
            }

            return redirect(url_for('views.education'))
        except Exception as e:
            message = {
                'status': 'danger',
                'message': 'Error adding qualification : ' 
            }

    return render_template('forms/education/add-education.html', message=message)


@form.route('/add-service', methods=['GET', 'POST'])
@login_required
def addService():
    message = ''
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            userid = session['user_id']

            image = request.files['image']

            # fetch image extension
            image_ext = image.filename.split('.')[-1]

            date = date
            date = date.replace(':', '')
            date = date.replace(' ', '_')

            filename = session['username'] + '_service_' + \
                date + '.' + image_ext

            image.save(os.path.join(
                './rivey/static/uploads/services/', secure_filename(filename)))

            filename = 'uploads/services/' + filename

            # save to database
            service = Services(
                service_title=title, description=description, image=filename, user_id=userid)
            db.session.add(service)
            db.session.commit()

            message = {
                'status': 'success',
                'message': 'Service added successfully'
            }
        except Exception as e:
            message = {
                'status': 'danger',
                'message': 'Error adding service : ' 
            }

        return redirect(url_for('views.services'))
    return render_template('forms/services/add-service.html', message=message)


@form.route('/add-experience', methods=['GET', 'POST'])
@login_required
def addExperience():
    message = ''
    if request.method == 'POST':
        try:
            userid = session['user_id']
            company = request.form['company']
            position = request.form['position']
            description = request.form['description']
            start_date = request.form['start_date']
            is_current = False
            end_date = ""
            try:
                is_current = request.form['current']
                if is_current == 'on':
                    is_current = True
            except:
                end_date = request.form['end_date']
                is_current = False

            experience = Experience(company=company, position=position, description=description,
                                          start_date=start_date, end_date=end_date, is_current=is_current, user_id=userid)

            db.session.add(experience)
            db.session.commit()

            message = {
                'status': 'success',
                'message': 'Experience added successfully'
            }

            return redirect(url_for('views.experience'))
        except Exception as e:
            message = {
                'status': 'danger',
                'message': 'Error adding Experience : ' 
            }

    return render_template('forms/experience/add-experience.html', message=message)


@form.route('/about', methods=['GET', 'POST'])
@login_required
def addAbout():
    userId = session['user_id']
    firstname = lastname = nationality = title = about_me = position = resume = experience = image = profile_image = age = ""
    if request.method == 'POST':
        try:
            about = About.query.filter_by(user_id=userId).first()

            firstname = request.form['firstname']
            lastname = request.form['lastname']
            nationality = request.form['nationality']
            title = request.form['about_title']
            about_me = request.form['about_description']
            position = request.form['position']
            resume = request.files['resume']
            experience = request.form['experience']
            image = request.files['about_picture']
            profile_image = request.files['profile']
            age = request.form['age']

            resume_filename = ""
            image_filename = ""
            profile_image_filename = ""

            date = str(datetime.now())
            date = date.replace(':', '')
            date = date.replace(' ', '_')

            if resume.filename != "":
                # fetch image extension
                resume_ext = resume.filename.split('.')[-1]

                filename = session['username'] + '_resume_' + \
                    date + '.' + resume_ext

                resume.save(os.path.join(
                    './rivey/static/uploads/resume/', secure_filename(filename)))

                resume_filename = 'uploads/resume/' + filename

            if image.filename != "":
                # fetch image extension
                image_ext = image.filename.split('.')[-1]

                filename = session['username'] + '_image_' + \
                    date + '.' + image_ext

                image.save(os.path.join(
                    './rivey/static/uploads/about/', secure_filename(filename)))

                image_filename = 'uploads/about/' + filename

            if profile_image.filename != "":
                # fetch image extension
                profile_image_ext = profile_image.filename.split('.')[-1]

                filename = session['username'] + '_profile_image_' + \
                    date + '.' + profile_image_ext

                profile_image.save(os.path.join(
                    './rivey/static/uploads/profile_image/', secure_filename(filename)))

                profile_image_filename = 'uploads/profile_image/' + filename

            if about is None:
                new_about = About(firstname=firstname, lastname=lastname, nationality=nationality, about_title=title, about_me=about_me, position=position,
                                  resume=resume_filename, experience=experience, image=image_filename, profile_image=profile_image_filename, age=age, user_id=userId)

                db.session.add(new_about)
                db.session.commit()

            else:
                about.firstname = firstname
                about.lastname = lastname
                about.nationality = nationality
                about.about_title = title
                about.about_me = about_me
                about.position = position
                about.resume = resume_filename
                about.experience = experience
                about.age = age

                if image.filename != "":
                    about.image = image_filename
                if profile_image.filename != "":
                    about.profile_image = profile_image_filename

                db.session.commit()

            return redirect(url_for('form.addAbout'))
        except Exception as e:

            return redirect(url_for('form.addAbout'))
    else:
        about = About.query.filter_by(user_id=userId).first()
        return render_template('forms/about_me/about.html', about=about)


@form.route('/social', methods=['GET', 'POST'])
@login_required
def addSocial():
    userId = session['user_id']

    facebook = twitter = instagram = linkedin = github = behance = dribbble = pinterest = youtube = stackoverflow = ""

    if request.method == 'POST':
        try:
            social = Social.query.filter_by(user_id=userId).first()

            facebook = request.form['facebook']
            twitter = request.form['twitter']
            instagram = request.form['instagram']
            linkedin = request.form['linkedin']
            github = request.form['github']
            behance = request.form['behance']
            dribble = request.form['dribble']
            pinterest = request.form['pinterest']
            youtube = request.form['youtube']
            stackoverflow = request.form['stackoverflow']

            if social is None:
                social = Social(facebook=facebook, twitter=twitter, instagram=instagram, linkedin=linkedin, github=github,behance=behance, dribble=dribble, pinterest=pinterest, youtube=youtube,stackoverflow=stackoverflow, user_id=userId)
                db.session.add(social)
                db.session.commit()

            else:
                social.facebook = facebook
                social.twitter = twitter
                social.instagram = instagram
                social.linkedin = linkedin
                social.github = github
                social.behance = behance
                social.dribble = dribble
                social.pinterest = pinterest
                social.youtube = youtube
                social.stackoverflow = stackoverflow

                db.session.commit()

            return redirect(url_for('form.addSocial'))
        except Exception as e:
            
            return redirect(url_for('form.addSocial'))
    else:
        social = Social.query.filter_by(user_id=userId).first()
        return render_template('forms/about_me/social-info.html', social=social)


@form.route('/add-project-category', methods=['POST', 'GET'], defaults={'id': None})
@form.route('/edit-project-category/<id>', methods=['GET'])
@login_required
def addProjectCategory(id):
    try:
        catId = id
    except:
        catId = None
    userId = session['user_id']

    cat = ""

    # check if skill id is present in the table or not
    if request.method == 'POST':
        try:
            name = request.form['title']

            try:
                catId = request.form['id']
            except:
                catId = None

            if catId != None and catId != "":
                cat = ProjectCategory.query.get(int(catId))
                cat.name = name
                db.session.commit()
            else:
                new_cat = ProjectCategory(name=name, user_id=userId)
                db.session.add(new_cat)
                db.session.commit()

            return redirect(url_for('views.project_category'))
        except Exception as e:

            return redirect(url_for('form.addProjectCategory'))
    else:
        # fetch skill from id
        if catId != None:
            print("cat is not noen")
            try:
                cat = ProjectCategory.query.get(int(catId))

                if cat is None:
                    message = {
                        'status': 'danger',
                        'message': 'Skill category not found'
                    }
                    return redirect(url_for('views.project_category'))

                return render_template('forms/projects/add-category.html', cat=cat)
            except Exception as e:

                return redirect(url_for('views.project_category'))

        else:
            return render_template('forms/projects/add-category.html', cat=cat)


@form.route('/add-project', methods=['POST', 'GET'], defaults={'id': None})
@form.route('/edit-project/<id>', methods=['GET'])
@login_required
def addProject(id):
    try:
        projectId = id
    except:
        projectId = None

    userId = session['user_id']

    project = ""
    filename  = ""

    # check if project id is present in the table or not
    if request.method == 'POST':
        try:
            title = request.form['title']
            name = request.form['name']
            description = request.form['description']
            link = request.form['link']
            client = request.form['client']
            category = request.form['category']
            image = request.files['image']

            try:
                projectId = request.form['id']
            except:
                projectId = None

            if projectId != None and projectId != "":
                project = Projects.query.get(int(projectId))
                project.project_title = title
                project.name = name
                project.description = description
                project.link = link
                project.client = client
                project.category_id = category

                if image.filename != "":
                    # fetch image extension
                    image_ext = image.filename.split('.')[-1]

                    date = str(datetime.now())
                    date = date.replace(':', '')
                    date = date.replace(' ', '_')

                    filename = session['username'] + '_project_' + \
                        date + '.' + image_ext

                    image.save(os.path.join(
                        './rivey/static/uploads/projects/', secure_filename(filename)))

                    filename = 'uploads/projects/' + filename

                    project.image = filename
                db.session.commit()
            else:
                if image.filename != "":
                    # fetch image extension
                    image_ext = image.filename.split('.')[-1]

                    date = str(datetime.now())
                    date = date.replace(':', '')    
                    date = date.replace(' ', '_')

                    filename = session['username'] + '_project_' + \
                        date + '.' + image_ext

                    image.save(os.path.join(
                        './rivey/static/uploads/projects/', secure_filename(filename)))

                    filename = 'uploads/projects/' + filename

                new_project = Projects(project_title=title, name=name, description=description, link=link, client=client, category_id=category,
                                       image=filename, user_id=userId)
                db.session.add(new_project)
                db.session.commit()

            return redirect(url_for('views.projects'))
        except Exception as e:
            
            return redirect(url_for('form.addProject'))
    else:
        # fetch project from id
        if projectId != None and projectId != "":
            
            try:
                project = Projects.query.get(int(projectId))

                if project is None:
                    message = {
                        'status': 'danger',
                        'message': 'Skill category not found'
                    }
                    return redirect(url_for('views.projects'))
                
                cat = ProjectCategory.query.filter_by(user_id=userId).all()

                return render_template('forms/projects/add-project.html', project=project, cat=cat)
            except Exception as e:
                return redirect(url_for('views.projects'))
        else:

            project = ""
            cat = ProjectCategory.query.filter_by(user_id=userId).all()
            return render_template('forms/projects/add-project.html', project="", cat=cat)


@form.route('/add-skill-category', methods=['POST', 'GET'], defaults={'id': None})
@form.route('/edit-skill-category/<id>', methods=['GET'])
@login_required
def addSkillCategory(id):
    try:
        catId = id
    except:
        catId = None
    userId = session['user_id']

    cat = ""

    # check if skill id is present in the table or not
    if request.method == 'POST':
        try:
            name = request.form['title']

            try:
                catId = request.form['id']
            except:
                catId = None

            if catId != None and catId != "":
                cat = SkillCategory.query.get(int(catId))
                cat.name = name
                db.session.commit()
            else:
                new_cat = SkillCategory(name=name, user_id=userId)
                db.session.add(new_cat)
                db.session.commit()

            return redirect(url_for('views.skill_category'))
        except Exception as e:

            return redirect(url_for('form.addSkillCategory'))
    else:
        # fetch skill from id
        if catId != None:
            try:
                cat = SkillCategory.query.get(int(catId))

                if cat is None:
                    message = {
                        'status': 'danger',
                        'message': 'Skill category not found'
                    }
                    return redirect(url_for('views.skill_category'))

                return render_template('forms/skills/add-category.html', cat=cat)
            except Exception as e:

                return redirect(url_for('views.skill_category'))

        else:
            return render_template('forms/skills/add-category.html', cat=cat)


@form.route('/add-skill', methods=['POST', 'GET'], defaults={'id': None})
@form.route('/edit-skill/<id>', methods=['GET'])
@login_required
def addSkill(id):
    try:
        skillId = id
    except:
        skillId = None

    userId = session['user_id']

    skill = ""

    # check if skill id is present in the table or not
    if request.method == 'POST':
        try:
            name = request.form['name']
            percentage = request.form['percentage']
            category = request.form['category']

            try:
                skillId = request.form['id']
            except:
                skillId = None

            if skillId != None and skillId != "":
                skill = Skills.query.get(int(skillId))
                skill.name = name
                skill.percentage = percentage
                skill.category_id = category
                db.session.commit()
            else:
                new_skill = Skills( name=name, percentage=percentage, category_id=category, user_id=userId)
                db.session.add(new_skill)
                db.session.commit()

            return redirect(url_for('views.skills'))
        except Exception as e:
            
            return redirect(url_for('form.addSkill'))
    else:
        # fetch skill from id
        if skillId != None:
            try:
                skill = Skills.query.get(int(skillId))

                if skill is None:
                    message = {
                        'status': 'danger',
                        'message': 'Skill category not found'
                    }
                    return redirect(url_for('views.skills'))
                
                cat = SkillCategory.query.filter_by(user_id=userId).all()

                return render_template('forms/skills/add-skill.html', skill=skill, cat=cat)
            except Exception as e:
                

                return redirect(url_for('views.skills'))
        else:
            cat = SkillCategory.query.filter_by(user_id=userId).all()
            return render_template('forms/skills/add-skill.html', skill=skill, cat=cat)


@form.route('/website-setting', methods=['GET', 'POST'])
@login_required
def websiteSettings():
    userId = session['user_id']

    if request.method == "POST":
        try:
            website = WebsiteSetting.query.filter_by(user_id=userId).first()

            title = request.form['title']
            seo = request.form['seo']
            email = request.form['email']
            logo = request.files['logo']
            favicon = request.files['favicon']

            date = str(datetime.now())
            date = date.replace(':', '')
            date = date.replace(' ', '_')

            logo_filename = ""
            favicon_filename = ""

            if logo.filename != "":
                # fetch image extension
                logo_ext = logo.filename.split('.')[-1]

                filename = session['username'] + '_logo_' + \
                    date + '.' + logo_ext

                logo.save(os.path.join(
                    './rivey/static/uploads/logo/', secure_filename(filename)))

                logo_filename = 'uploads/logo/' + filename

            if favicon.filename != "":
                # fetch image extension
                favicon_ext = favicon.filename.split('.')[-1]

                filename = session['username'] + '_favicon_' + \
                    date + '.' + favicon_ext

                favicon.save(os.path.join(
                    './rivey/static/uploads/favicon/', secure_filename(filename)))

                favicon_filename = 'uploads/favicon/' + filename

            if website is None:
                website = WebsiteSetting(web_title=title, seo=seo, email=email,
                                         logo=logo_filename, favicon=favicon_filename, user_id=userId)
                db.session.add(website)
                db.session.commit()
            else:
                website.web_title = title
                website.seo = seo
                website.email = email

                if logo.filename != "":
                    website.logo = logo_filename
                if favicon.filename != "":
                    website.favicon = favicon_filename

                db.session.commit()

            return redirect(url_for('form.websiteSettings'))
        except Exception as e:

            return redirect(url_for('form.websiteSettings'))
    else:
        website = WebsiteSetting.query.filter_by(user_id=userId).first()

        return render_template('forms/website.html', website=website)


@form.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    # check if user id is present in the table or not
    if request.method == 'POST':
        try:
            userId = session['user_id']

            contact = Contact.query.filter_by(user_id=userId).first()

            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            lat = request.form['lat']
            lng = request.form['lng']

            if contact is None:
                contact = Contact(
                    email=email, phone=phone, address=address, lat=lat, lng=lng, user_id=userId)
                db.session.add(contact)
                db.session.commit()
            else:
                contact.email = email
                contact.phone = phone
                contact.address = address
                contact.lat = lat
                contact.lng = lng

                db.session.commit()

            return redirect(url_for('form.contact'))
        except:
            return redirect(url_for('form.contact'))
    else:
        userId = session['user_id']

        contact = Contact.query.filter_by(user_id=userId).first()

        return render_template('forms/about_me/contact.html', contact=contact)


# # #
# # #
# Edit Routes with id as parameter
# # #
# # #

@form.route('/edit-education/<id>', methods=['GET'])
@form.route('/edit-education', methods=['POST'], defaults={'id': None})
@login_required
def editEducation(id):
    message = ''

    if request.method == 'POST':
        try:
            id = request.form['id']
            school = request.form['school']
            field = request.form['field']
            description = request.form['description']
            start_date = request.form['start-date']
            is_current = False

            try:
                is_current = request.form['current-study']
                if is_current == 'on':
                    is_current = True

                    education = Qualification.query.get(int(id))
                    education.school = school
                    education.field = field
                    education.description = description
                    education.start_date = start_date
                    education.is_current = is_current

            except:
                end_date = request.form['end-date']

                education = Qualification.query.get(int(id))
                education.school = school
                education.field = field
                education.description = description
                education.start_date = start_date
                education.end_date = end_date
                education.is_current = is_current

            db.session.commit()

            message = {
                'status': 'success',
                'message': 'Service updated successfully'
            }
        except Exception as e:
            message = {
                'status': 'danger',
                'message': 'Error updating service: ' 
            }
        return redirect(url_for('views.education'))
    else:
        # fetch service from id
        if id != None:
            education = Qualification.query.get(int(id))

            if education is None:
                message = {
                    'status': 'danger',
                    'message': 'Qualification not found'
                }
                return redirect(url_for('views.education'))

            return render_template('forms/education/edit-education.html', e=education)


@form.route('/edit-experience/<id>', methods=['GET'])
@form.route('/edit-experience', methods=['POST'], defaults={'id': None})
@login_required
def editExperience(id):
    message = ''

    if request.method == 'POST':
        try:
            id = request.form['id'] 
            company = request.form['company']
            position = request.form['position']
            description = request.form['description']
            start_date = request.form['start_date']
            is_current = False
            end_date = ""

            try:
                is_current = request.form['current']
                if is_current == 'on':
                    is_current = True
            except:
                try:
                    end_date = request.form['end_date']
                except:
                    end_date = ""
                is_current = False

            print("+======================")
            print(id)
            print("=========================")

                
            experience = Experience.query.get(int(id))
            experience.company = company
            experience.position = position
            experience.description = description
            experience.start_date = start_date
            experience.end_date = end_date
            experience.is_current = is_current

            db.session.commit()

            message = {
                'status': 'success',
                'message': 'Experience updated successfully'
            }
        except Exception as e:
            
            message = {
                'status': 'danger',
                'message': 'Error updating experience: ' 
            }
        return redirect(url_for('views.experience'))
    else:
        # fetch service from id
        if id != None:
            experience = Experience.query.get(int(id))

            if experience is None:
                message = {
                    'status': 'danger',
                    'message': 'Experience not found'
                }
                return redirect(url_for('views.experience'))

            return render_template('forms/experience/edit-experience.html', experience=experience)


@form.route('/edit-service/<id>', methods=['GET'])
@form.route('/edit-service', methods=['POST'], defaults={'id': None})
@login_required
def editService(id):
    message = ''

    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            serviceId = request.form['service_id']
            image = request.files['image']

            date = str(datetime.now())
            date = date.replace(':', '')
            date = date.replace(' ', '_')

            if image.filename != "":
                # fetch image extension
                image_ext = image.filename.split('.')[-1]

                filename = session['username'] + '_service_' + \
                    date + '.' + image_ext

                image.save(os.path.join(
                    './rivey/static/uploads/services/', secure_filename(filename)))

                filename = 'uploads/services/' + filename

            # update to database
            service = Services.query.get(int(serviceId))
            service.service_title = title
            service.description = description
            if image.filename != "":
                service.image = filename

            db.session
            db.session.commit()

            message = {
                'status': 'success',
                'message': 'service updated successfully'
            }
        except Exception as e:
            message = {
                'status': 'danger',
                'message': 'Error updating service: ' 
            }
        return redirect(url_for('views.services'))
    else:
        # fetch service from id
        if id != None:
            service = Services.query.get(int(id))

            if service is None:
                message = {
                    'status': 'danger',
                    'message': 'Service not found'
                }
                return redirect(url_for('views.services'))

            return render_template('forms/services/edit-service.html', service=service)


# # #
# # #
# delete data
# # #
# # #

@form.route('/delete-education/<id>')
@login_required
def deleteEducation(id):
    try:
        education = Qualification.query.get(int(id))

        db.session.delete(education)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Qualification deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting qualification: ' 
        }

    return redirect(url_for('views.education'))


@form.route('/delete-experience/<id>')
@login_required
def deleteExperience(id):
    try:
        experience = Experience.query.get(int(id))

        db.session.delete(experience)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Experience deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting experience: ' 
        }

    return redirect(url_for('views.experience'))


@form.route('/delete-service/<id>')
@login_required
def deleteService(id):
    try:
        service = Services.query.get(int(id))

        db.session.delete(service)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Service deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting service: ' 
        }

    return redirect(url_for('views.services'))


@form.route('/delete-project/<id>')
@login_required
def deleteProject(id):
    try:
        project = Projects.query.get(int(id))

        db.session.delete(project)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Project deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting project: ' 
        }

    return redirect(url_for('views.projects'))


@form.route('/delete-skill/<id>')
@login_required
def deleteSkill(id):
    try:
        skill = Skills.query.get(int(id))

        db.session.delete(skill)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Skill deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting skill: ' 
        }

    return redirect(url_for('views.skills'))


@form.route('/delete-skill-category/<id>')
@login_required
def deleteSkillCategory(id):
    try:
        cat = SkillCategory.query.get(int(id))

        db.session.delete(cat)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Skill category deleted successfully'
        }

    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting skill category: ' 
        }

    return redirect(url_for('views.skill_category'))


@form.route('/delete-project-category/<id>')
@login_required
def deleteProjectCategory(id):

    try:
        cat = ProjectCategory.query.get(int(id))

        db.session.delete(cat)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Project category deleted successfully'
        }

    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting project category: ' 
        }

    return redirect(url_for('views.project_category'))

# delete messagge


@form.route('/delete-message/<id>')
@login_required
def deleteMessage(id):
    try:
        message = Messages.query.get(int(id))

        db.session.delete(message)
        db.session.commit()

        message = {
            'status': 'success',
            'message': 'Message deleted successfully'
        }
    except Exception as e:
        message = {
            'status': 'danger',
            'message': 'Error deleting message: ' 
        }

    return redirect(url_for('views.messages'))
