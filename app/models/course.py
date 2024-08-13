from app import db
from sqlalchemy import Column, Integer, String, Numeric, LargeBinary
from sqlalchemy.orm import relationship

class Course(db.Model):
    __tablename__ = 'courses'
    courses_id = db.Column(db.Integer, primary_key=True)
    courses_title = db.Column(db.String(144), unique=False)
    courses_content = db.Column(db.String(500), unique=False, nullable=True)
    courses_image = db.Column(db.LargeBinary, unique=False, nullable=True)
    courses_price = db.Column(Numeric(10, 2), unique=False)
    courses_discounted_price = db.Column(Numeric(10, 2), unique=False, nullable=True)
    courses_professor_id = db.Column(db.Integer, db.ForeignKey('professors.professors_id'))
    courses_studycenter_id = db.Column(db.Integer, db.ForeignKey('studycenters.studyCenters_id'))
    courses_category_id = db.Column(db.Integer, db.ForeignKey('categories.categories_id'))

    professor = db.relationship('Professor', backref=db.backref('courses', lazy='dynamic'))
    enrollments = db.relationship('Enrollment',  back_populates='course')  
    studycenter = db.relationship('StudyCenter', backref=db.backref('courses', lazy='dynamic'))
    category = relationship('Category', back_populates='courses',  foreign_keys=[courses_category_id])

    
    def __init__(self, courses_title, courses_content, courses_image, courses_price, courses_discounted_price, courses_professor_id, courses_studycenter_id, courses_category_id):
        self.courses_title = courses_title
        self.courses_content = courses_content
        self.courses_image = courses_image
        self.courses_price = courses_price
        self.courses_discounted_price = courses_discounted_price
        self.courses_professor_id = courses_professor_id
        self.courses_studycenter_id = courses_studycenter_id
        self.courses_category_id = courses_category_id
