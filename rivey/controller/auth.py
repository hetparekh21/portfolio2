from flask import Blueprint, render_template, request, session, url_for, redirect
from rivey.firebase import firebase_init
from rivey.models import User
from rivey import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta
from rivey.controller import views

authv = Blueprint('authv', __name__)

auth = firebase_init()

@authv.route('/login', methods=['GET', 'POST'])
def login():
    clearUser()
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_info = auth.get_account_info(user['idToken'])

            # check if email is verified
            if user_info['users'][0]['emailVerified'] == False:
                message = {
                    'status': 'danger',
                    'message': 'Please verify your email first'
                }
            else:  
                session['email'] = user['email']
                session['refresh_token'] = user['refreshToken']

                dbuser = User.query.filter_by(email=email).first()
                if dbuser!=None:
                    login_user(dbuser, remember=True, duration=timedelta(minutes=60))

                session['username'] = dbuser.username
                session['user_id'] = dbuser.id                
                
                message = {
                    'status': 'success',
                    'message': 'Logged in successfully'
                }

                return redirect(url_for('views.home'))
            
        except Exception as e:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(e).__name__, e.args)
            message = {
                'status': 'danger',
                'message': 'Invalid email or password'
            }

    return render_template('auth/login.html', message=message)

@authv.route('/signup', methods=['GET', 'POST'])
def signup():
    clearUser()

    message = ""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        
        # or query to check if email or username already exists
        dbuser = User.query.filter_by(username=username).first()
        
        if dbuser==None:
            try:
                user = auth.create_user_with_email_and_password(email=email, password=password)
                auth.send_email_verification(user['idToken'])

                # add user to database
                new_user = User(email=email, username=username)
                db.session.add(new_user)
                db.session.commit()

                message = {
                    'status': 'success',
                    'message': 'Account created successfully, please check your email inbox to verify your account'
                }
                return render_template('auth/login.html', message=message)
            except:
                message = {
                    'status': 'danger',
                    'message': 'Something went wrong, please try again'
                }

        else:
            message = {
                'status': 'danger',
                'message': 'Username already exists'
            }
    return render_template('auth/register.html', message=message)

@authv.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    message = ""
    if request.method == "POST":
        email = request.form.get('email')
        try:
            auth.send_password_reset_email(email)
            message = {
                'status': 'success',
                'message': 'Password reset email sent, please check your email inbox'
            }
        except:
            message = {
                'status': 'danger',
                'message': 'Something went wrong, please try again'
            }
            return render_template('auth/forgot-password.html', message=message)
        
        return render_template('auth/login.html', message=message)
    return render_template('auth/forgot-password.html', message=message)

@authv.route('/logout',methods=['GET'])
@login_required
def logout():
    clearUser()
    return redirect(url_for('authv.login'))

def clearUser():
    auth.current_user = None
    logout_user() 
    session.clear()

@authv.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
    message = ""
    email = session['email']
    try:
        auth.send_password_reset_email(email)
        message = {
            'status': 'success',
            'message': 'Password reset email sent, please check your email inbox'
        }
    except:
        message = {
            'status': 'danger',
            'message': 'Something went wrong, please try again'
        }

    return render_template('forms/edit-profile.html', message=message)