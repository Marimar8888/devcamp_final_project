from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class StudyCenter(db.Model):
    __tablename__ = 'studycenters'
    studyCenters_id = db.Column(db.Integer, primary_key=True)
    studyCenters_name = db.Column(db.String(144), unique=False, nullable=False)
    studyCenters_email = db.Column(db.String(80), unique=True, nullable=False)
    studyCenters_user_id = db.Column(db.Integer,  db.ForeignKey('users.users_id'),  nullable=False)

    studycenter_students= relationship('StudyCenterStudent', back_populates='studyCenter')

    def __init__(self, studyCenters_name, studyCenters_email, studyCenters_user_id):
        self.studyCenters_name = studyCenters_name
        self.studyCenters_email =  studyCenters_email
        self.studyCenters_user_id = studyCenters_user_id

