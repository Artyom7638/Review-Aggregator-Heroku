import os
import random

from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
from cheroot.ssl.pyopenssl import pyOpenSSLAdapter
from database import db
from src import app, Config, init_db_categories_and_services
from src.models.master import Master
from src.models.category import Category
from src.models.service import Service

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_LOCAL_MY_SQL_DB
app.config['WTF_CSRF_ENABLED'] = False
app.config['FLASK_DEBUG'] = 0
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    if not Category.query.all():
        init_db_categories_and_services()
    if not Master.query.all():
        for i in range(100):
            num = random.randint(1, 16)
            c = Service.query.get(num)
            m = Master(name='test', surname='test', services=[])
            m.services.append(c)
            db.session.add(m)
            db.session.commit()
    db.session.commit()
testing_app = app
testing_db = db


port = int(os.environ.get('PORT', 8100))
server = WSGIServer(('0.0.0.0', port), app)
adapter = pyOpenSSLAdapter(certificate="certificate.pem", private_key="certificate_private_key.pem")
# server.ssl_adapter = adapter


if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
