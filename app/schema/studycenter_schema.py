from app import ma
from app.models.study_center import StudyCenter

class StudyCenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenter
        load_instance = True
        include_relationships = True