from database import db


class Service(db.Model):
    __tablename__ = 'service'
    __table_args__ = (
        db.UniqueConstraint('category_id', 'name'),
    )
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(50))
    masters = db.relationship("Master", secondary='master_service', back_populates="services")
