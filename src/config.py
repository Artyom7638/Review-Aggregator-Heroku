import os


class Config:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    TEMPLATE_FOLDER = os.path.join(ROOT, 'src', 'templates')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ROOT, 'database.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@localhost/schema'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector' + os.environ.get('CLEARDB_DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = os.path.join(ROOT, 'photos')
    WORK_PHOTOS_RESOLUTION = (800, 800)
    AVATARS_RESOLUTION = (400, 400)
    MAX_CONTENT_LENGTH = 1024 * 1024 * 3  # 1024^2 = MB
    MAX_PHOTOS_SPACE_PER_MASTER = 20  # MB
    REVIEWS_PER_PAGE = 3
    SEARCH_MASTERS_PER_PAGE = 6
    SECRET_KEY = os.urandom(32)
    BCRYPT_LOG_ROUNDS = 11
    MIN_AMOUNT_OF_REVIEWS_FOR_RATING = 1
    '''
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('LOGIN', 'name')
    MAIL_PASSWORD = os.environ.get('PASSWORD', 'password')
    '''
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'name@gmail.com')  # необходимо чтоб знать с какой почты отправлять
    SENDGRID_USERNAME = os.environ.get('SENDGRID_USERNAME')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'None')
    EMAIL_CONFIRMATIONS_DISABLED = False
    WTF_CSRF_ENABLED = False
