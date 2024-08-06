from app import db

class UserRol(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rols.rols_id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('rols', lazy='dynamic'))
    rol = db.relationship('Rol', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, user_id, rol_id):
        self. user_id = user_id
        self.rol_id = rol_id