from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class StudyCenter(db.Model):
    __tablename__ = 'studycenters'
    studyCenters_id = db.Column(db.Integer, primary_key=True)
    studyCenters_name = db.Column(db.String(144), unique=False, nullable=False)
    studyCenters_email = db.Column(db.String(80), unique=True, nullable=False)
    studyCenters_user_id = db.Column(db.Integer,  db.ForeignKey('users.users_id'),  nullable=False)
    studyCenters_cif = db.Column(db.String(9), nullable=False, unique=True)
    studyCenters_address = db.Column(db.String(255), nullable=False)
    studyCenters_city = db.Column(db.String(50), nullable=False)
    studyCenters_postal = db.Column(db.Integer, nullable=False)
    studyCenters_number_card = db.Column(db.String(16), nullable=False)
    studyCenters_exp_date = db.Column(db.String(5), nullable=False)
    studyCenters_cvc = db.Column(db.Integer, nullable=False)
    studyCenters_active = db.Column(db.Boolean, default=True)

    studycenter_students= relationship('StudyCenterStudent', back_populates='studyCenter')

    def __init__(
        self, studyCenters_name, studyCenters_email, studyCenters_user_id, studyCenters_address, studyCenters_city,
        studyCenters_postal, studyCenters_number_card, studyCenters_exp_date, studyCenters_cvc, studyCenters_cif, studyCenters_active):
        self.studyCenters_name = studyCenters_name
        self.studyCenters_email =  studyCenters_email
        self.studyCenters_user_id = studyCenters_user_id
        self.studyCenters_address = studyCenters_address
        self.studyCenters_city = studyCenters_city
        self.studyCenters_postal = studyCenters_postal
        self.studyCenters_number_card = studyCenters_number_card
        self.studyCenters_exp_date = studyCenters_exp_date
        self.studyCenters_cvc = studyCenters_cvc
        self.studyCenters_cif = studyCenters_cif
        self.studyCenters_active = studyCenters_active
 

