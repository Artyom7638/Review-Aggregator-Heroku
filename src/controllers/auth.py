import os

from flasgger import swag_from
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from database import db
from src import Config
from src.forms.auth.client_registration_form import ClientRegistrationForm
from src.forms.auth.login_form import LogInForm
from src.forms.auth.master_registration_form import MasterRegistrationForm
from src.forms.search.search_form import SearchForm
from src.models.master import Master
from src.models.category import Category
from src.models.client import Client
from src.models.service import Service
from src.models.user import User
from time import time
import jwt
from flask_mail import Message
from mail import mail
from threading import Thread
from datetime import datetime


auth = Blueprint('auth', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'auth'))


@auth.route('/login', methods=['GET', 'POST'])
@swag_from('yml/login_get.yml', methods=['GET'])
@swag_from('yml/login_post.yml', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LogInForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.check_password(login_form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next:
                for r in current_app.url_map._rules:
                    if r.rule == next:
                        return redirect(next)
            return redirect(url_for('main.index'))
        login_form.errors['form'] = ['Неверный логин или пароль']
    return render_template('login.html', title='Авторизация', login_form=login_form)


@auth.route("/logout")
@login_required
@swag_from('yml/logout.yml')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/registration/client', methods=['GET', 'POST'])
@swag_from('yml/registration_client_get.yml', methods=['GET'])
@swag_from('yml/registration_client_post.yml', methods=['POST'])
def client_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    registration_form = ClientRegistrationForm()
    if registration_form.validate_on_submit():
        user = User.query.filter_by(email=registration_form.email.data).first()
        if not user:
            client = Client(email=registration_form.email.data, name=registration_form.name.data,
                            surname=registration_form.surname.data)
            client.set_password(registration_form.password.data)
            db.session.add(client)
            db.session.commit()
            login_user(client)
            if Config.EMAIL_CONFIRMATIONS_DISABLED:
                client.email_confirmed = True
            else:
                send_email_confirmation()
                client.email_confirmation_sent_date = datetime.now()
            db.session.commit()
            return redirect(url_for('main.index'))
        registration_form.errors['email'] = ['На данную почту уже зарегистрирован пользователь']
    return render_template('client_registration.html', title='Регистрация пользователя',
                           registration_form=registration_form)


@auth.route('/registration/master', methods=['GET', 'POST'])
@swag_from('yml/registration_master_get.yml', methods=['GET'])
@swag_from('yml/registration_master_post.yml', methods=['POST'])
def master_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    registration_form = MasterRegistrationForm()
    t = request
    if registration_form.validate_on_submit():
        user = User.query.filter_by(email=registration_form.email.data).first()
        if not user:
            master = Master(email=registration_form.email.data, name=registration_form.name.data,
                            surname=registration_form.surname.data, phone_number=registration_form.phone_number.data)
            master.set_password(registration_form.password.data)
            master.services = Service.query.filter(Service.id.in_(registration_form.services.data)).all()
            db.session.add(master)
            db.session.commit()
            login_user(master)
            if Config.EMAIL_CONFIRMATIONS_DISABLED:
                master.email_confirmed = True
            else:
                send_email_confirmation()
                master.email_confirmation_sent_date = datetime.now()
            db.session.commit()
            return redirect(url_for('main.index'))
        registration_form.errors['email'] = ['На данную почту уже зарегистрирован пользователь']
    categories = {category.name: category for category in Category.query.all()}
    return render_template('master_registration.html', title='Регистрация мастера', categories=categories,
                           registration_form=registration_form)


@auth.route('/confirm-email/<token>')
@login_required
@swag_from('yml/confirm_email.yml')
def confirm_email(token):
    id = verify_reset_password_token(token)
    confirmed = False
    if id:
        user = Client.query.get(id)
        if user:
            confirmed = True
            user.email_confirmed = True
            db.session.commit()
    return render_template('email_confirmed.html', title='Подтверждение почты', resend_email=False, confirmed=confirmed,
                           search_form=SearchForm(), dont_insert_libraries=True)


@auth.route('/resend-email')
@login_required
@swag_from('yml/resend_email.yml')
def resend_email():
    if current_user.email_confirmed:
        return redirect(url_for('main.index'))
    delta = datetime.now() - current_user.email_confirmation_sent_date
    successfully_sent = False
    if delta.total_seconds() > 3600:
        send_email_confirmation()
        current_user.email_confirmation_sent_date = datetime.now()
        db.session.commit()
        successfully_sent = True
    return render_template('email_confirmed.html', title='Подтверждение почты', resend_email=True,
                           successfully_sent=successfully_sent, search_form=SearchForm(), dont_insert_libraries=True)


def send_email_confirmation():
    token = get_token(current_user)
    recipients = [current_user.email]
    send_email('Подтверждение почты для BeautyYou', sender=("BeautyYou", Config.EMAIL_ADDRESS),
               recipients=recipients, text_body=render_template('email_confirmation.txt', user=current_user, token=token),
               html_body=render_template('email_confirmation.html', user=current_user, token=token))
    return redirect(url_for('main.index'))


def send_async_email(msg, context):
    with context:
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(msg, current_app.app_context())).start()


def get_token(user, expires_in=3600):  # 3600 секунд
    return jwt.encode({'id': user.id, 'exp': time() + expires_in}, Config.SECRET_KEY, algorithm='HS256').decode('utf-8')


def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['id']
        return id
    except:
        return None
