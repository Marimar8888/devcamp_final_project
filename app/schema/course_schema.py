from app import ma
from app.models.course import Course

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_relationships = True
        exclude = ('enrollments',)

class CourseBasicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_relationships = False
        clude = ('enrollments', 'studycenter', 'professor', 'category', 'favorited_by')
