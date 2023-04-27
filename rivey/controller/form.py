from flask import Blueprint, render_template

form = Blueprint('form', __name__)

@form.route('/edit-profile')
def editProfile():
    return render_template('forms/edit-profile.html')


###
# Add Routes
###
@form.route('/add-education')
def addEducation():
    return render_template('forms/education/add-education.html')

@form.route('/add-service')
def addService():
    return render_template('forms/services/add-service.html')

@form.route('/add-testimonial')
def addTestimonial():
    return render_template('forms/testimonial/add-testimonial.html')

@form.route('/add-client')
def addClient():
    return render_template('forms/clients/add-client.html')

@form.route('/add-experience')
def addExperience():
    return render_template('forms/experience/add-experience.html')


###
# Edit Routes with id as parameter
###
@form.route('/edit-education/<id>')
def editEducation(id):
    return render_template('forms/education/edit-education.html', id=id)

@form.route('/edit-service/<id>')
def editService(id):
    return render_template('forms/services/edit-service.html', id=id)

@form.route('/edit-testimonial/<id>')
def editTestimonial(id):
    return render_template('forms/testimonial/edit-testimonial.html', id=id)

@form.route('/edit-client/<id>')
def editClient(id):
    return render_template('forms/clients/edit-client.html', id=id)

@form.route('/edit-experience/<id>')
def editExperience(id):
    return render_template('forms/experience/edit-experience.html', id=id)  