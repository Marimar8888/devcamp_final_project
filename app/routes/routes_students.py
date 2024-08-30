from flask import Blueprint, request, jsonify
from app.models import Student, Enrollment, Course
from app.schema.student_schema import StudentSchema
from app.models import User, UserRol, Rol
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

    required_fields = [
        'students_first_name', 'students_last_name', 'students_user_id', 'students_dni', 'students_address',
        'students_city', 'students_postal', 'students_number_card', 'students_exp_date', 'students_cvc'
        ]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    students_first_name = data['students_first_name']
    students_last_name = data['students_last_name']
    students_user_id = data['students_user_id']
    students_dni = data['students_dni']
    students_address = data['students_address']
    students_city = data['students_city']
    students_postal = data['students_postal']
    students_number_card = data['students_number_card']
    students_exp_date = data['students_exp_date']
    students_cvc = data['students_cvc']

    existing_student = Student.query.filter_by(students_user_id=students_user_id).first()
    if existing_student:
        return jsonify({'error': 'El estudiante ya existe'}), 400

    new_student = Student(
        students_first_name=students_first_name, students_last_name=students_last_name, students_user_id=students_user_id,
        students_dni = students_dni, students_address = students_address, students_city = students_city, students_postal = students_postal,
        students_number_card = students_number_card, students_exp_date = students_exp_date, students_cvc = students_cvc
    )
    
    try:
        db.session.add(new_student)
        db.session.commit()
        student_rol = Rol.query.get(2)
        if student_rol is None:
            return jsonify({'error': 'Rol not found'}), 404
        student_rol_entry = UserRol(user_id=new_student.students_user_id, rol_id=student_rol.rols_id)
        db.session.add(student_rol_entry) 
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
        'students_dni': student.students_dni,
        'students_address': student.students_address,
        'students_city': student.students_city,
        'students_postal': student.students_postal,
        'students_number_card': student.students_number_card,
        'students_exp_date': student.students_exp_date,
        'students_cvc': student.students_cvc,
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
    student.students_dni = data.get('students_dni', student.students_dni)
    student.students_address = data.get('students_address', student.students_address)
    student.students_city = data.get('students_city', student.students_city)
    student.students_postal = data.get('students_postal', student.students_postal)
    student.students_number_card = data.get('students_number_card', student.students_number_card)
    student.students_exp_date = data.get('students_exp_date', student.students_exp_date)
    student.students_cvc = data.get('students_cvc', student.students_cvc)

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

    UserRol.query.filter_by(user_id=student.students_user_id, rol_id=2).delete()
    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': 'Student deleted'})


@bp.route("/student/user_id/<user_id>", methods=["GET"])
def get_student_by_user_id(user_id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    student = Student.query.filter_by(students_user_id=user_id).first()

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    return jsonify({'students_id': student.students_id})
