from app import db
from sqlalchemy import Column, Integer, ForeignKey

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollments_id = db.Column(db.Integer, primary_key=True)
    enrollments_student_id = db.Column(db.Integer, db.ForeignKey('students.students_id'))
    enrollments_course_id = db.Column(db.Integer, db.ForeignKey('courses.courses_id'))

    student = db.relationship('Student', back_populates='enrollments')  
    course = db.relationship('Course', back_populates='enrollments')

    def __init__(self, enrollments_student_id, enrollments_course_id):
        self.enrollments_student_id = enrollments_student_id
        self.enrollments_course_id = enrollments_course_id
