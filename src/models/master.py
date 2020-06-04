from database import db
from src.models.client import Client


class Master(Client):
    __tablename__ = 'master'
    id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    phone_number = db.Column(db.String(20))
    short_description = db.Column(db.String(250), default='')
    description = db.Column(db.String(2000), default='')
    photos = db.relationship('Photo', lazy='dynamic', foreign_keys='Photo.master_id')
    services = db.relationship("Service", secondary='master_service', back_populates="masters")
    reviews_about_master = db.relationship('Review', backref='master', lazy='dynamic', foreign_keys='Review.master_id')
    average_rating = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'master',
    }
