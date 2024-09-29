from app import ma
from app.models.professor import Professor

class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Professor
        load_instance = True
        include_relationships = True
        exclude = ('professor_students', 'studycenters',)
        

class ProfessorBasicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Professor
        load_instance = True
        include_relationships = False

