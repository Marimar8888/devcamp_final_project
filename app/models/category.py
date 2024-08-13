from app import db
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

class Category(db.Model):
    __tablename__ = 'categories'
    categories_id = db.Column(db.Integer, primary_key=True)
    categories_name = db.Column(db.String(144), unique=True, nullable=False)

    courses = relationship('Course', back_populates='category', foreign_keys='Course.courses_category_id')

def __init__(self, categories_name):
    self.categories_name = categories_name
