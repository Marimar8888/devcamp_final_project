from marshmallow import Schema, fields
from app.models.student import Student
from app.schema.course_schema import CourseSchema

class StudentSchema(Schema):

    students_id = fields.Int()
    students_first_name = fields.Str()
    students_last_name = fields.Str()
    students_email = fields.Str()
    students_user_id = fields.Int()
    students_dni = fields.Str()
    students_address = fields.Str()
    students_city = fields.Str()
    students_postal = fields.Int()
    students_number_card = fields.Str()
    students_exp_date = fields.Str()
    students_cvc = fields.Int()

    courses = fields.List(fields.Nested(CourseSchema, exclude=('enrollments',)))
    
    class Meta:
        model = Student
        load_instance = True
        include_relationships = True
