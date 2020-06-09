import os

from flasgger import swag_from
from flask import render_template, Blueprint
from sqlalchemy import func
from sqlalchemy.sql import text
from database import db
from src import Config
from src.forms.search.search_form import SearchForm
from src.models import Master
from src.models.client import Client
from src.models.review import Review

main = Blueprint('main', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'main'))


@main.route('/')
@swag_from('yml/index.yml')
def index():
    c = Client.query.get(21)
    c.email_confirmed = True
    db.session.commit()
    m = db.session.query(Master, func.count(Review.id).label('total')).outerjoin(Review).\
        filter(Master.is_not_blocked.is_(True)).group_by(Master).order_by(text('total DESC')).limit(3).all()
    masters = [master[0] for master in m]
    reviews = Review.query.join(Client).filter(Client.is_not_blocked.is_(True)).order_by(func.random()).limit(3).all()
    return render_template('index.html', title='Главная', search_form=SearchForm(), masters=masters, reviews=reviews)
