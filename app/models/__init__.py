from .user import User
from .rol import Rol
from .course import Course
from .professor import Professor  
from .study_center import StudyCenter
from .student import Student
from .category import Category
from .professor_studycenter import ProfessorStudyCenter
from .user_rol import UserRol
from .enrollment import Enrollment
from .studycenter_student import StudyCenterStudent
from .professor_student import ProfessorStudent
from app.schema.user_schema import UserSchema, LoginUserSchema  
from app.schema.professor_schema import ProfessorSchema
from app.schema.course_schema import CourseSchema
from app.schema.studycenter_schema import StudyCenterSchema
from app.schema.professor_studycenter_schema import ProfessorStudyCenterSchema 
from app.schema.rol_schema import RolSchema
from app.schema.category_schema import CategorySchema
from app.schema.user_rol_schema import UserRolSchema
from app.schema.enrollment_schema import EnrollmentSchema
from app.schema.studycenter_student_schema import StudyCenterStudentSchema
from app.schema.professor_student_schema import ProfessorStudentSchema

def get_category_schema():
    return CategorySchema()

def get_professor_schema():
    return ProfessorSchema()

def get_studycenter_schema():
    return StudyCenterSchema()

def get_user_schema():
    return UserSchema()

def get_login_user_schema():  
    return LoginUserSchema()

def get_rol_schema():
    return RolSchema()

def get_user_rol_schema():
    return UserRolSchema()

def get_enrollment_schema():
    return EnrollmentSchema()

def get_professor_studycenter_schema():
    return ProfessorStudentSchema()


__all__ = [
    'User', 'Course', 'Professor', 'StudyCenter', 'ProfessorStudyCenter', 'Student', 'Enrollment', 'StudyCenterStudent', 'Category',
    'get_professor_schema', 'get_studycenter_schema', 'get_professor_studycenter_schema', 'get_user_schema', 'get_rol_schema', 
    'get_user_rol_schema', 'get_enrollment_schema', 'get_professor_studycenter_schema', 'get_category_schema'
]

