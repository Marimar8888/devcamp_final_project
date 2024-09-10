from app import ma
from app.models.study_center import StudyCenter

class StudyCenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyCenter
        load_instance = True
        include_relationships = False
        fields = ('studyCenters_id', 'studyCenters_name', 'studyCenters_email', 'studyCenters_user_id')

class StudyCenterDetailSchema(ma.SQLAlchemyAutoSchema):
   
    students = ma.Nested('StudentSchema', many=True)  

    class Meta:
        model = StudyCenter
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ('studycenter_students', 'courses', 'professors')