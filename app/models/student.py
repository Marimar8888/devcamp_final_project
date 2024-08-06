from app import db

class Student(db.Model):
    __tablename__ = 'students'
    students_id = db.Column(db.Integer, primary_key=True)
    students_first_name = db.Column(db.String(144), unique=False, nullable=False)
    students_last_name = db.Column(db.String(144), unique=False, nullable=False)
    students_user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), unique=True, nullable=False)

 
    def __init__(self, students_first_name, students_last_name, students_user_id):
        self.students_first_name = students_first_name
        self.students_last_name = students_last_name
        self.students_user_id = students_user_id
