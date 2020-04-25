from flask_login import UserMixin

from b_crypt import bcrypt
from database import db


class User(UserMixin, db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    type = db.Column(db.String(20))
    password_hash = db.Column(db.String(500))
    name = db.Column(db.String(25))
    surname = db.Column(db.String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def set_password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)
