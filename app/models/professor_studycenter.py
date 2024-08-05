from app import db

class ProfessorStudyCenter(db.Model):
    __tablename__ = 'professor_studycenter'
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.professors_id'), primary_key=True)
    studycenter_id = db.Column(db.Integer, db.ForeignKey('studycenters.studyCenters_id'), primary_key=True)

    professor = db.relationship('Professor', backref=db.backref('studycenters', lazy='dynamic'))
    studycenter = db.relationship('StudyCenter', backref=db.backref('professors', lazy='dynamic'))

    def __init__(self, professor_id, studycenter_id):
        self.professor_id = professor_id
        self.studycenter_id = studycenter_id
