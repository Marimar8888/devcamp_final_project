from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Professor(db.Model):
    __tablename__ = 'professors'
    professors_id = db.Column(db.Integer, primary_key=True)
    professors_first_name = db.Column(db.String(144), nullable=False)
    professors_last_name = db.Column(db.String(144))
    professors_email = db.Column(db.String(80), unique=True, nullable=False)
    professors_user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), unique=True, nullable=False)
    professors_dni = db.Column(db.String(9), nullable=False, unique=True)
    professors_address = db.Column(db.String(255), nullable=False)
    professors_city = db.Column(db.String(50), nullable=False)
    professors_postal = db.Column(db.Integer, nullable=False)
    professors_number_card = db.Column(db.String(16), nullable=False)
    professors_exp_date = db.Column(db.String(5), nullable=False)
    professors_cvc = db.Column(db.Integer, nullable=False)

    professor_students = relationship('ProfessorStudent', back_populates='professor')

    def __init__(self, professors_first_name, professors_last_name, professors_email, professors_user_id, professors_dni, professors_address, professors_city, 
        professors_postal, professors_number_card, professors_exp_date, professors_cvc):
        self.professors_first_name = professors_first_name
        self.professors_last_name = professors_last_name
        self.professors_email = professors_email
        self.professors_user_id = professors_user_id
        self.professors_dni = professors_dni
        self.professors_address = professors_address
        self.professors_city = professors_city
        self.professors_postal = professors_postal
        self.professors_number_card = professors_number_card
        self.professors_exp_date = professors_exp_date
        self.professors_cvc = professors_cvc