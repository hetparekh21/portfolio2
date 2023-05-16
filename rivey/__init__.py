# all imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta

# creating database
db = SQLAlchemy()
DB_NAME = "rivey.db"
UPLOAD_FOLDER = '/rivey/static/uploads'


# main function to create flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DEV'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # adding configuration for using a sqlite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.permanent_session_lifetime = timedelta(minutes=60)
        
    # routes
    from .controller.views import views
    from .controller.form import form
    from .controller.error import error
    from .controller.auth import authv

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(form, url_prefix='/')
    app.register_blueprint(error, url_prefix='/')
    app.register_blueprint(authv, url_prefix='/')

    # calling create_database function
    create_database(app)

    # setting up login manager
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'authv.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# function to create database if not exists
def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')