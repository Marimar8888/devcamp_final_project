from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Rol(db.Model):
    __tablename__ = 'rols'
    rols_id = Column(Integer, primary_key=True)
    rols_name = Column(String(20), unique=True, nullable=False)

    user_roles = relationship('UserRol', back_populates='rol')  

    def __init__(self, rols_name):
        self.rols_name = rols_name

    