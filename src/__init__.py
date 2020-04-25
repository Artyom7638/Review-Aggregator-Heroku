from werkzeug.middleware.dispatcher import DispatcherMiddleware

from b_crypt import bcrypt
from login_manager import login_manager
from src.config import Config
from flask import Flask
from database import db
from src.controllers.review import review
from src.controllers.search import search_blueprint
from src.controllers.auth import auth
from src.controllers.main import main, handle_exceptions
from src.controllers.profile import profile
from src.models.service import Service
from src.models.category import Category
from src.models.moderator import Moderator


def init_db_categories_and_services():
    hair_care = Category(name='Уход за волосами')
    nail_care = Category(name='Уход за ногтями')
    massage_spa = Category(name='Массаж, SPA')
    skin_care = Category(name='Уход за кожей')
    tattoos = Category(name='Татуировки')
    piercing = Category(name='Пирсинг')
    for c in [hair_care, nail_care, massage_spa, skin_care, tattoos, piercing]:
        db.session.add(c)
    db.session.commit()
    id = hair_care.id
    hair_care_services = [Service(name='Стрижка', category_id=id), Service(name='Окрашивание', category_id=id),
                          Service(name='Мелирование', category_id=id), Service(name='Укладка', category_id=id)]
    id = nail_care.id
    nail_care_services = [Service(name='Маникюр', category_id=id), Service(name='Педикюр', category_id=id),
                          Service(name='Наращивание ногтей', category_id=id)]
    id = massage_spa.id
    massage_spa_services = [Service(name='Массаж', category_id=id), Service(name='SPA', category_id=id),
                            Service(name='Тайский массаж', category_id=id)]
    id = skin_care.id
    skin_care_services = [Service(name='Удаление прыщей', category_id=id), Service(name='Чистка кожи', category_id=id)]
    id = tattoos.id
    tattoos_services = [Service(name='Цветные татуировки', category_id=id),
                        Service(name='Монохромные татуировки', category_id=id),
                        Service(name='Удаление татуировок', category_id=id)]
    id = piercing.id
    piercing_services = [Service(name='Пирсинг головы', category_id=id), Service(name='Пирсинг тела', category_id=id)]
    db.session.bulk_save_objects(hair_care_services)
    db.session.bulk_save_objects(nail_care_services)
    db.session.bulk_save_objects(massage_spa_services)
    db.session.bulk_save_objects(skin_care_services)
    db.session.bulk_save_objects(tattoos_services)
    db.session.bulk_save_objects(piercing_services)
    db.session.commit()


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
with app.app_context():
    db.create_all()
    categories = Category.query.all()
    if not categories:
        init_db_categories_and_services()
    '''
    moder = Moderator(email='t3@ya.ru')
    moder.set_password('ttttt')
    db.session.add(moder)
    db.session.commit()
    '''
bcrypt.init_app(app)
app.register_blueprint(main)
app.register_blueprint(search_blueprint)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(review)
# app.register_error_handler(404, lambda x: render_error(404))
# app.register_error_handler(500, lambda x: render_error(500))
app.register_error_handler(Exception, handle_exceptions)


@app.errorhandler(404)
def not_found(e):
    return "404"
'''
if not os.path.isdir(Config.UPLOAD_FOLDER):
    os.mkdir(Config.UPLOAD_FOLDER, 0o744)
'''
