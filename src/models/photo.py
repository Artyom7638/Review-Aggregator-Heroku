import os
from flask import url_for
from database import db
from src.config import Config


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'))
    path = db.Column(db.String(50))

    def get_photo_url(self):
        return url_for('profile.photo', id=self.id)

    def get_photos_folder_path(self):
        return os.path.join(Config.UPLOAD_FOLDER, str(self.master_id))

    def get_photo_path(self):
        folder = self.get_photos_folder_path()
        return os.path.join(folder, self.path)
