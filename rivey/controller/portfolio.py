from flask import Blueprint, render_template, session
from rivey import db

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/portfolio/<id>')
def portfolio_page(id):
    pass
