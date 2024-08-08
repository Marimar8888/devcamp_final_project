from app import db

class StudyCenterStudent(db.Model):
    __tablename__ = 'studycenter_student'
    studycenter_student_id = db.Column(db.Integer, primary_key= True)
    studycenter_student_student_id = db.Column(db.Integer, db.ForeignKey('students.students_id'))
    studycenter_student_center_id = db.Column(db.Integer, db.ForeignKey('studycenters.studyCenters_id'))
    
    studyCenter = db.relationship('StudyCenter', backref=db.backref('students', lazy='dynamic'))
    student = db.relationship('Student', backref=db.backref('studeycenters', lazy='dynamic'))

    def __init__(self, studycenter_student_student_id, studycenter_student_center_id):
        self.studycenter_student_student_id = studycenter_student_student_id
        self.studycenter_student_center_id =  studycenter_student_center_id