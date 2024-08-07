from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UserRol(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rols.rols_id'), primary_key=True)

    user = relationship('User', back_populates='user_roles')
    rol = relationship('Rol', back_populates='user_roles')

    def __init__(self, user_id, rol_id):
        self. user_id = user_id
        self.rol_id = rol_id