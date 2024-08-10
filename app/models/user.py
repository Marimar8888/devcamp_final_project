from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'
    users_id = Column(Integer, primary_key=True)
    users_name = Column(String(100), nullable=False)
    users_email = Column(String(80), unique=True, nullable=False)
    users_password = Column(String(64), nullable=False)


    user_roles = relationship('UserRol', back_populates='user')  

    def __init__(self, users_name, users_email, users_password):
        self.users_name = users_name
        self.users_email = users_email
        self.users_password = users_password

