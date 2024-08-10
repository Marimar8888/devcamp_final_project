from flask import Blueprint, request, jsonify
from app.models import Student, Course, Enrollment
from app.schema.enrollment_schema import EnrollmentSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token

from app import db

bp = Blueprint('enrollment', __name__)

enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)

@bp.route('/enrollment', methods=['POST'])
def add_enrollment():

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    data = request.json

    required_fields = ['enrollments_student_id', 'enrollments_course_id', 'enrollments_start_date', 'enrollments_end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400
    
    enrollments_student_id = data['enrollments_student_id']
    enrollments_course_id = data['enrollments_course_id']
    enrollments_start_date = data['enrollments_start_date']
    enrollments_end_date = data['enrollments_end_date']

    student = Student.query.get(enrollments_student_id)
    course = Course.query.get(enrollments_course_id)

    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    existing_relationship = Enrollment.query.filter_by(
        enrollments_student_id = enrollments_student_id, 
        enrollments_course_id =  enrollments_course_id
    ).first()

    if existing_relationship:
        return jsonify({'error': 'Ya has realizado este curso'}), 400
    
    new_relationship = Enrollment(
         enrollments_student_id = enrollments_student_id, 
         enrollments_course_id =  enrollments_course_id,
         enrollments_start_date = enrollments_start_date,
         enrollments_end_date = enrollments_end_date
        )

    try:
        db.session.add( new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se puede matricular en este curso', 'details': str(e)}), 500
    
    return jsonify({'message': 'Contratación del curso exitosa'}), 201
    
@bp.route('/enrollments', methods=["GET"])
def all_enrollments():

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    all_enrollments = Enrollment.query.all()
    result = enrollments_schema.dump(all_enrollments)
    return jsonify(result)

@bp.route('/enrollment/<id>', methods=["GET"])
def get_enrollment(id):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    return enrollment_schema.jsonify(enrollment)

@bp.route('/enrollment/<id>', methods=["PUT"])
def update_enrollment(id):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    data = request.json
    enrollment.enrollments_student_id = data.get('enrollments_student_id',  enrollment.enrollments_student_id)
    enrollment.enrollments_course_id = data.get('enrollments_course_id', enrollment.enrollments_course_id)
    enrollment.enrollments_start_date = data.get('enrollments_start_date', enrollment.enrollments_start_date)
    enrollment.enrollments_end_date = data.get('enrollments_end_date', enrollment.enrollments_end_date)
    db.session.commit()

    return enrollment_schema.jsonify(enrollment)

@bp.route('/enrollment/<id>', methods=["DELETE"])
def delete_enrollment(id):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({'message': 'La matricula del curso se ha eliminado correctamente.'})