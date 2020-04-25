from database import db


class MasterService(db.Model):
    __tablename__ = 'master_service'
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), primary_key=True)
