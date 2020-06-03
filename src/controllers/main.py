import os
from flask import render_template, Blueprint, url_for, current_app
from werkzeug.exceptions import InternalServerError

from src import Config
from src.forms.search.search_form import SearchForm


main = Blueprint('main', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'main'))


@main.route('/')
def index():
    return render_template('index.html', title='Главная', search_form=SearchForm())


def handle_exceptions(e):
    return f"{e.__class__.__name__}: {e}"

