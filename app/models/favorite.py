from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorites_user_id = Column(db.Integer, db.ForeignKey('users.users_id'),  primary_key=True)
    favorites_course_id = Column(db.Integer, db.ForeignKey('courses.courses_id'), primary_key=True)

    user = db.relationship('User', backref = db.backref('favorites', lazy=True))
    course = db.relationship('Course', backref = db.backref('favorited_by', lazy=True))

    def __init__(self, favorites_user_id, favorites_course_id):
        self.favorites_user_id = favorites_user_id
        self.favorites_course_id = favorites_course_id

