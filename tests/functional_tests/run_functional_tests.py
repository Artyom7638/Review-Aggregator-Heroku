import os

from flask_login import login_user, current_user

from src import init_db_categories_and_services
from src.models import Master
from src.models.service import Service
from src.models.category import Category
from src.models.client import Client
from tests.functional_tests.review_test import test_review_rights
from tests.functional_tests.test_login import test_login
from tests.functional_tests.test_search import test_search


def init(app, db):
    with app.app_context():
        db.create_all()
        if not Category.query.all():
            init_db_categories_and_services()
        user = Client(email='test@test.com')
        user.set_password('test_password')
        db.session.add(user)
        user = Client(email='client@client.com', type='client', is_not_blocked=True, email_confirmed=True, reviews=[])
        user.set_password('test_password')
        db.session.add(user)
        user = Master(email='master@master.com', name='master', surname='master', type='master', is_not_blocked=True, email_confirmed=True, reviews=[])
        user.set_password('test_password')
        db.session.add(user)
        hair_1 = Service.query.filter_by(name='Окрашивание').first()
        nail_1 = Service.query.filter_by(name='Педикюр').first()
        tattoos_0 = Service.query.filter_by(name='Цветные татуировки').first()
        hair_0 = Service.query.filter_by(name='Стрижка').first()
        massage_0 = Service.query.filter_by(name='Массаж').first()
        piercing_0 = Service.query.filter_by(name='Пирсинг головы').first()
        master1 = Master(name='Ольга', surname='Иванова',
                         services=[hair_1, nail_1, tattoos_0])
        master2 = Master(name='Ольга', surname='Петрова', services=[tattoos_0])
        master3 = Master(name='Екатерина', surname='Бородина',
                         services=[hair_0, massage_0, piercing_0])
        db.session.add(master1)
        db.session.add(master2)
        db.session.add(master3)
        db.session.commit()


def destruct(app, db, db_path=None):
    with app.app_context():
        db.drop_all()
        if db_path:  # sqlite
            os.remove(db_path)


def run_functional_tests(app, db, db_path=None):
    init(app, db)
    with app.test_client() as test_client:
        with app.app_context():
            test_login(test_client)
    destruct(app, db)

    init(app, db)
    with app.test_client() as test_client:
        with app.app_context():
            #with test_client.session_transaction() as session:
            test_review_rights(test_client, db)
    destruct(app, db)

    init(app, db)
    try:
        with app.test_client() as test_client:
            with app.app_context():
                test_search(test_client, db)
    except Exception as e:
        print(e)
        destruct(app, db)
    destruct(app, db)
