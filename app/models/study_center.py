from app import db

class StudyCenter(db.Model):
    __tablename__ = 'studycenters'
    studyCenters_id = db.Column(db.Integer, primary_key=True)
    studyCenters_name = db.Column(db.String(144), unique=False, nullable=False)
    studyCenters_email = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, studyCenters_name, studyCenters_email):
        self.studyCenters_name = studyCenters_name
        self. studyCenters_email =  studyCenters_email

