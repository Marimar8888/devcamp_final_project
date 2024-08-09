from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class StudyCenterStudent(db.Model):
    __tablename__ = 'studycenter_student'
    studycenter_student_id = db.Column(db.Integer, primary_key= True)
    studycenter_student_student_id = db.Column(db.Integer, db.ForeignKey('students.students_id'))
    studycenter_student_center_id = db.Column(db.Integer, db.ForeignKey('studycenters.studyCenters_id'))
    
    studyCenter = db.relationship('StudyCenter',  back_populates='studycenter_students')
    student = db.relationship('Student', back_populates='studycenter_students')

    def __init__(self, studycenter_student_student_id, studycenter_student_center_id):
        self.studycenter_student_student_id = studycenter_student_student_id
        self.studycenter_student_center_id =  studycenter_student_center_id