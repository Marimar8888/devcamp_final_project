from app import ma
from app.models import ProfessorStudyCenter

class ProfessorStudyCenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProfessorStudyCenter
        load_instance = True
        include_fk = True