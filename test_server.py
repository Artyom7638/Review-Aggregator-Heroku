import os
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
from cheroot.ssl.pyopenssl import pyOpenSSLAdapter
from database import db
from src import app, Config, init_db_categories_and_services


app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_LOCAL_MY_SQL_DB
app.config['WTF_CSRF_ENABLED'] = False
app.config['FLASK_DEBUG'] = 0
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
testing_app = app
testing_db = db


port = int(os.environ.get('PORT', 8100))
server = WSGIServer(('0.0.0.0', port), app)


if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
