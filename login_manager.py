from flask import url_for, request
from flask_login import LoginManager
from werkzeug.utils import redirect

from src.models.client import Client

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login', next=request.path))


@login_manager.user_loader
def load_user(id):
    return Client.query.get(int(id))
