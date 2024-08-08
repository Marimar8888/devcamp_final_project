from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class ProfessorStudent(db.Model):
    professor_student_id = db.Column(db.Integer, primary_key=True)
    professor_student_professor_id = db.Column(db.Integer, ForeignKey('professors.professors_id'))
    professor_student_student_id = db.Column(db.Integer, ForeignKey('students.students_id'))
    
    professor = db.relationship('Professor', back_populates='professor_students')
    student = db.relationship('Student', back_populates='professor_students')

    def __init__(self, professor_student_professor_id, professor_student_student_id):
        self.professor_student_professor_id = professor_student_professor_id
        self.professor_student_student_id = professor_student_student_id
       