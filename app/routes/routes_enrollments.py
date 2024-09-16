from flask import Blueprint, request, jsonify
from app.models import Student, Course, Enrollment
from app.schema.enrollment_schema import EnrollmentSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token
from datetime import datetime

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
        
    data = request.form 

    required_fields = ['enrollments_student_id', 'enrollments_course_ids', 'enrollments_start_date', 'enrollments_end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    enrollments_student_id = data.get('enrollments_student_id')
    enrollments_course_ids = request.form.getlist('enrollments_course_ids') 
    enrollments_start_date = datetime.strptime(data['enrollments_start_date'], '%Y-%m-%d %H:%M:%S')
    enrollments_end_date = datetime.strptime(data['enrollments_end_date'], '%Y-%m-%d %H:%M:%S')

    student = Student.query.get(enrollments_student_id)

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    if not enrollments_course_ids:
        return jsonify({'error': 'Debe proporcionar al menos un curso'}), 400

    new_enrollment_code = Enrollment.generate_enrollments_code()

    successful_enrollments = []
    errors = []

    for course_id in enrollments_course_ids:
        course = Course.query.get(course_id)

        if not course:
            errors.append(f'Course with id {course_id} not found')
            continue

        existing_relationship = Enrollment.query.filter_by(
            enrollments_student_id = enrollments_student_id, 
            enrollments_course_id = course_id
        ).first()

        if existing_relationship:
            errors.append(f'Ya estás inscrito en el curso con id {course_id}')
            continue

        new_relationship = Enrollment(
            enrollments_student_id = enrollments_student_id, 
            enrollments_course_id = course_id,
            enrollments_start_date = enrollments_start_date,
            enrollments_end_date = enrollments_end_date,
            enrollments_finalized=False,
        )
        new_relationship.enrollments_code = new_enrollment_code 

        try:
            db.session.add(new_relationship)
            db.session.commit()
            successful_enrollments.append({
                'course_id': course_id,
                'enrollments_code': new_relationship.enrollments_code 
            })
        except Exception as e:
            db.session.rollback()
            errors.append(f'Error al matricularse en el curso con id {course_id}: {str(e)}')

    if successful_enrollments:
        message = {
            'message': 'Contratación exitosa de los cursos',
            'successful_enrollments': successful_enrollments
        }
        if errors:
            message['errors'] = errors
        return jsonify(message), 201
    else:
        return jsonify({'error': 'No se pudo matricular en ningún curso', 'details': errors}), 400
   
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
    
    return enrollment_schema.jsonify(enrollment), 200

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
    enrollment.enrollments_finalized = data.get('enrollments_finalized', enrollment.enrollments_finalized)
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