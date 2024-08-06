from app import ma
from app.models.course import Course

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_relationships = True