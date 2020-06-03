import os


class Config:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    TEMPLATE_FOLDER = os.path.join(ROOT, 'src', 'templates')
    STATIC_TEMPLATES_FOLDER = 'static/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ROOT, 'database.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@localhost/schema'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = os.path.join(ROOT, 'images')
    TEMP_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'temp')
    # IMAGES_RESOLUTION = (500, 500)
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10  # 1024^2 = MB
    REVIEWS_PER_PAGE = 3
    SEARCH_MASTERS_PER_PAGE = 6
    SECRET_KEY = "bv-=534[]{}ho{]423[]gd!@#&^%@!"  # исправить плюс проверить отключение дебага
    BCRYPT_LOG_ROUNDS = 11
    MIN_AMOUNT_OF_REVIEWS_FOR_RATING = 2
    # SERVER_NAME = 'ip:port'
