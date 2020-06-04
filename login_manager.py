from flask import url_for, request
from flask_login import LoginManager
from werkzeug.utils import redirect
from src.models.user import User

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login', next=request.path))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
