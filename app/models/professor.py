from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Professor(db.Model):
    __tablename__ = 'professors'
    professors_id = db.Column(db.Integer, primary_key=True)
    professors_name = db.Column(db.String(100), nullable=False)
    professors_email = db.Column(db.String(80), unique=True, nullable=False)

    professor_students = relationship('ProfessorStudent', back_populates='professor')

    def __init__(self, professors_name, professors_email):
        self.professors_name = professors_name
        self.professors_email = professors_email
