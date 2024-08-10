from flask import Blueprint, request, jsonify
from app.models import Student, Enrollment, Course
from app.schema.student_schema import StudentSchema
from app import db

from app.config import Config
from app.utils.token_manager import decode_token, encode_token

# Definir el blueprint para las rutas de User
bp = Blueprint('students', __name__)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@bp.route('/student', methods=["POST"])
def add_student():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    data = request.json

    required_fields = ['students_first_name', 'students_last_name', 'students_user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    students_first_name = data['students_first_name']
    students_last_name = data['students_last_name']
    students_user_id = data['students_user_id']

    existing_student = Student.query.filter_by(students_user_id=students_user_id).first()
    if existing_student:
        return jsonify({'error': 'El estudiante ya existe'}), 400

    new_student = Student(students_first_name=students_first_name, students_last_name=students_last_name, students_user_id=students_user_id)
    
    try:
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el estudiante', 'details': str(e)}), 500

    student = Student.query.get(new_student.students_id)

    return jsonify(student_schema.dump(student)), 201

    
@bp.route('/students', methods=["GET"])
def all_students():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    
    return jsonify(result)

@bp.route("/student/<id>", methods=["GET"])
def get_student(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    enrollments = Enrollment.query.filter_by(enrollments_student_id = id). all()
    courses = [Course.query.get(enrollment.enrollments_course_id) for enrollment in enrollments]

    student_schema_with_courses = {
        'students_id': student.students_id,
        'students_first_name': student.students_first_name,
        'students_last_name': student.students_last_name,
        'students_user_id': student.students_user_id,
        'courses': [{'courses_id': course.courses_id,
                     'courses_title': course.courses_title,
                     'courses_content': course.courses_content,
                     'courses_image': course.courses_image,
                     'courses_price': course.courses_price,
                     'courses_discounted_price': course.courses_discounted_price,
                     'courses_professor_id': course.courses_professor_id,
                     'courses_studycenter_id': course.courses_studycenter_id}
                    for course in courses]
    }

    return jsonify(student_schema_with_courses)

@bp.route("/student/<id>", methods=["PUT"])
def update_student(id):
    
    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    data = request.json
    student.students_first_name = data.get('students_first_name', student.students_first_name)
    student.students_last_name = data.get('students_last_name', student.students_last_name)
    student.students_user_id = data.get('students_user_id', student.students_user_id)

    db.session.commit()

    return jsonify(student_schema.dump(student))

@bp.route("/student/<id>", methods=["DELETE"])
def delete_student(id):
    
    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': 'Student deleted'})