from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Student(db.Model):
    __tablename__ = 'students'
    students_id = db.Column(db.Integer, primary_key=True)
    students_first_name = db.Column(db.String(144), unique=False, nullable=False)
    students_last_name = db.Column(db.String(144), unique=False, nullable=False)
    students_user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), unique=True, nullable=False)
    students_dni = db.Column(db.String(9), nullable=True)
    students_address = db.Column(db.String(255), nullable=True)
    students_city = db.Column(db.String(50), nullable=True)
    students_postal = db.Column(db.Integer, nullable=True)
    students_number_card = db.Column(db.String(16), nullable=True)
    students_exp_date = db.Column(db.String(5), nullable=True)
    students_cvc = db.Column(db.Integer, nullable=True)


    enrollments = relationship('Enrollment', back_populates='student')
    professor_students = relationship('ProfessorStudent', back_populates='student') 
    studycenter_students = relationship('StudyCenterStudent', back_populates = 'student') 
       
    def __init__(self, students_first_name, students_last_name, students_user_id, students_dni, students_address, students_city, students_postal, students_number_card, students_exp_date, students_cvc):
        self.students_first_name = students_first_name
        self.students_last_name = students_last_name
        self.students_user_id = students_user_id
        self.students_dni = students_dni
        self.students_address = students_address
        self.students_city = students_city
        self.students_postal = students_postal
        self.students_number_card = students_number_card
        self.students_exp_date = students_exp_date
        self.students_cvc = students_cvc