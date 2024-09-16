from app import db
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from datetime import datetime

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollments_id = db.Column(db.Integer, primary_key=True)
    enrollments_student_id = db.Column(db.Integer, db.ForeignKey('students.students_id'), nullable=False)
    enrollments_course_id = db.Column(db.Integer, db.ForeignKey('courses.courses_id'), nullable=False)
    enrollments_start_date = db.Column(db.DateTime, nullable=False)
    enrollments_end_date =  db.Column(db.DateTime, nullable=False)
    enrollments_finalized = db.Column(db.Boolean, default=False, nullable=False)
    enrollments_code = db.Column(db.String(20), nullable=False)
    enrollments_price = db.Column(Numeric(10, 2), nullable=True)
  

    student = db.relationship('Student', back_populates='enrollments')  
    course = db.relationship('Course', back_populates='enrollments')

    def __init__(self, enrollments_student_id, enrollments_course_id, enrollments_start_date, enrollments_end_date, enrollments_price, enrollments_finalized=False):
        self.enrollments_student_id = enrollments_student_id
        self.enrollments_course_id = enrollments_course_id
        self.enrollments_start_date = enrollments_start_date
        self.enrollments_end_date = enrollments_end_date
        self.enrollments_price = enrollments_price
        self.enrollments_finalized = enrollments_finalized
        self.enrollments_code = None  

    
    @staticmethod
    def generate_enrollments_code():
        current_year = datetime.now().year 
        last_enrollment = Enrollment.query.order_by(Enrollment.enrollments_id.desc()).first()
        
        if last_enrollment:
            last_code = last_enrollment.enrollments_code.split('-')[0]
            new_code = int(last_code.split('-')[0]) + 1
            return f"{str(new_code).zfill(4)}-{current_year}"
        else:
           return f"0001-{current_year}"

   