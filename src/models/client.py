from flask_login import UserMixin

from b_crypt import bcrypt
from database import db
from src.models.user import User


class Client(User):
    __table_args__ = {'extend_existing': True}
    avatar_path = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='author', lazy='dynamic', foreign_keys='Review.author_id')
    # модератор

    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }

    def set_password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)
