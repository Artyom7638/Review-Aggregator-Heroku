import os
from flask import url_for
from database import db
from src.config import Config
from src.models.user import User
from datetime import datetime


class Client(User):
    __tablename__ = 'client'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    avatar_path = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='author', lazy='dynamic', foreign_keys='Review.author_id')
    is_not_blocked = db.Column(db.Boolean, default=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_sent_date = db.Column(db.DateTime, default=datetime.now)

    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }

    def get_avatar_url(self):
        return url_for('profile.avatar', id=self.id)

    def get_images_folder_path(self):
        return os.path.join(Config.UPLOAD_FOLDER, str(self.id))

    def get_avatar_path(self):
        if not self.avatar_path:
            return None
        folder = self.get_images_folder_path()
        return os.path.join(folder, self.avatar_path)
