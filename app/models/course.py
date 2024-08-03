from app import db, ma
from sqlalchemy import Numeric

class Course(db.Model):
    __tablename__ = 'courses'
    courses_id = db.Column(db.Integer, primary_key=True)
    courses_title = db.Column(db.String(144), unique=False)
    courses_content = db.Column(db.String(500), unique=False, nullable=True)
    courses_image = db.Column(db.LargeBinary, unique=False, nullable=True)
    courses_price = db.Column(Numeric(10, 2), unique=False)
    courses_discounted_price = db.Column(Numeric(10, 2), unique=False, nullable=True)
    
    def __init__(self,  courses_title,  courses_content, courses_image, courses_price, courses_discounted_price):
        self.courses_title = courses_title
        self.courses_content = courses_content
        self.courses_image = courses_image
        self.courses_price = courses_price
        self.courses_discounted_price = courses_discounted_price

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course