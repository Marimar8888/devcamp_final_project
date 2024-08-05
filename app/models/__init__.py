from .user import User, UserSchema 
from .course import Course, CourseSchema 
from .professor import Professor  
from .study_center import StudyCenter
from .professor_studycenter import ProfessorStudyCenter
from app.schema.professor_schema import ProfessorSchema
from app.schema.studycenter_schema import StudyCenterSchema
from app.schema.professor_studycenter_schema import ProfessorStudyCenterSchema 


def get_professor_schema():
    return ProfessorSchema()

def get_studycenter_schema():
    return StudyCenterSchema()

def get_professor_studycenter_schema():
    return ProfessorStudyCenterSchema()


__all__ = [
    'User', 'Course', 'Professor', 'StudyCenter', 'ProfessorStudyCenter', 'get_professor_schema', 'get_studycenter_schema', 'get_professor_studycenter_schema'
]

