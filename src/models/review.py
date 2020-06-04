from datetime import datetime
from database import db


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    rating = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'))
