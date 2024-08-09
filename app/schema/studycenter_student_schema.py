from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.studycenter_student import StudyCenterStudent

class StudyCenterStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenterStudent
        load_instance = True
        include_fk = True   