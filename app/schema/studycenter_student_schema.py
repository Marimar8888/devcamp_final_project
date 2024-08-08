from app import ma
from app.models import StudyCenterStudent

class StudyCenterStudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenterStudent
        load_instance = True
        include_fk = True