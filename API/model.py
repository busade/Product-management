from .utils import db
from datetime import datetime


class Products (db.Model):
    __tablename__ = "pms"
    id= db.Column(db.Integer(),primary_key = True)
    name= db.Column(db.String(45), nullable = False, unique= True)
    info = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime(),default=datetime.utcnow)
    quantity= db.Column(db.Integer(),nullable=False)

    def __repr__ (self):
        return f"Products{self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id): 
        return cls.query.get_or_404(id)