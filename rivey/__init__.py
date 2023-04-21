# all imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager

# main function to create flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DEV'

    return app