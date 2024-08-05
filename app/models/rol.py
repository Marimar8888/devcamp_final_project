from app import db

class Rol(db.Model):
    __tablename__='rols'
    rols_id = db.Column(db.Integer, primary_key=True)
    rols_name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, rols_name):
        self.rols_name = rols_name

    