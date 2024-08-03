from app import db, ma

class StudyCenter(db.Model):
    __tablename__ = 'studycenters'
    studyCenters_id = db.Column(db.Integer, primary_key=True)
    studyCenters_name = db.Column(db.String(144), unique=False, nullable=False)
    studyCenters_professor_id = db.Column(db.Integer, db.ForeignKey('professors.professors_id'), nullable=False)  
    studyCenters_email = db.Column(db.String(80), unique=True, nullable=False)

    professor = db.relationship('Professor', backref='studycenters', lazy=True)

    def __init__(self, studyCenters_name, studyCenters_professor_id, studyCenters_email):
        self.studyCenters_name = studyCenters_name
        self.studyCenters_professor_id = studyCenters_professor_id
        self. studyCenters_email =  studyCenters_email

    
class StudyCenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenter
        include_fk = True