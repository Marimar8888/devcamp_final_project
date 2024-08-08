from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.professor_student import ProfessorStudent

class ProfessorStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProfessorStudent
        load_instance = True
        include_fk = True