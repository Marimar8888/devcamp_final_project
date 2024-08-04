from app import db, ma

class StudyCenterProfessor(db.Model):
    
    __tablename__ = 'studycenter_professor'

    studycenter_id = db.Column(db.Integer, db.ForeignKey('studycenters.studyCenters_id'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.professors_id'), primary_key=True)

    studycenter = db.relationship('StudyCenter', back_populates='professors')
    professor = db.relationship('Professor', back_populates='studycenters')

 def __init__(self, studycenter_id, professor_id):
        self.studycenter_id = studycenter_id
        self.professor_id = professor_id
    
class StudyCenterProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenterProfessor
        include_fk = True

    studycenter = ma.Nested('StudyCenterSchema', exclude=['professors'])
    professor = ma.Nested('ProfessorSchema', exclude=['studycenters'])