import os

from flask import Blueprint, render_template, redirect, url_for, abort, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from database import db
from src import Config
from src.forms.auth.client_registration_form import ClientRegistrationForm
from src.forms.auth.login_form import LogInForm
from src.forms.auth.master_registration_form import MasterRegistrationForm
from src.models.master import Master
from src.models.category import Category
from src.models.client import Client
from src.models.service import Service

# auth = Blueprint('auth', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'auth'), subdomain="test.name")
auth = Blueprint('auth', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'auth'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LogInForm()
    if login_form.validate_on_submit():
        user = Client.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.check_password(login_form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next:
                for r in current_app.url_map._rules:
                    if r.rule == next:
                        return redirect(next)
            print(url_for('main.index'))
            print(url_for('main.index', _external=True))
            # return redirect('https://test.name' + url_for('main.index'))
            return redirect(url_for('main.index'))
        login_form.errors['form'] = ['Неверный логин или пароль']
    return render_template('login.html', title='Войти', login_form=login_form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/registration/client', methods=['GET', 'POST'])
def client_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    registration_form = ClientRegistrationForm()
    if registration_form.validate_on_submit():
        client = Client(email=registration_form.email.data, name=registration_form.name.data,
                        surname=registration_form.surname.data)
        client.set_password(registration_form.password.data)
        db.session.add(client)
        db.session.commit()
        login_user(client)
        return redirect(url_for('main.index'))
    return render_template('client_registration.html', title='Регистрация', registration_form=registration_form)


@auth.route('/registration/master', methods=['GET', 'POST'])
def master_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    registration_form = MasterRegistrationForm()
    if registration_form.validate_on_submit():
        master = Master(email=registration_form.email.data, name=registration_form.name.data,
                        surname=registration_form.surname.data, phone_number=registration_form.phone_number.data)
        master.set_password(registration_form.password.data)
        master.services = Service.query.filter(Service.id.in_(registration_form.services.data)).all()
        db.session.add(master)
        db.session.commit()
        login_user(master)
        return redirect(url_for('main.index'))
    categories = {category.name: category for category in Category.query.all()}
    return render_template('master_registration.html', title='Регистрация', categories=categories,
                           registration_form=registration_form)
