# all imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager

# main function to create flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DEV'

    # routes
    from .controller.views import views
    from .controller.form import form
    from .controller.error import error

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(form, url_prefix='/')
    app.register_blueprint(error, url_prefix='/')

    return app