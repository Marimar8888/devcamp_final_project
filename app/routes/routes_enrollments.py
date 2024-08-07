from flask import Blueprint, request, jsonify
from app.models import Student, Course, Enrollment
from app.schema.enrollment_schema import EnrollmentSchema

from app import db

bp = Blueprint('enrollment', __name__)

enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)

@bp.route('/enrollment', methods=['POST'])
def add_enrollment():
    data = request.json

    required_fields = ['enrollments_student_id', 'enrollments_course_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400
    
    enrollments_student_id = data['enrollments_student_id']
    enrollments_course_id = data['enrollments_course_id']

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
         enrollments_course_id =  enrollments_course_id
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
    all_enrollments = Enrollment.query.all()
    result = enrollments_schema.dump(all_enrollments)
    return jsonify(result)

@bp.route('/enrollment/<id>', methods=["GET"])
def get_enrollment(id):
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    return enrollment_schema.jsonify(enrollment)

@bp.route('/enrollment/<id>', methods=["PUT"])
def update_enrollment(id):
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    data = request.json
    enrollment.enrollments_student_id = data.get('enrollments_student_id',  enrollment.enrollments_student_id)
    enrollment.enrollments_course_id = data.get('enrollments_course_id', enrollment.enrollments_course_id)

    db.session.commit()

    return enrollment_schema.jsonify(enrollment)

@bp.route('/enrollment/<id>', methods=["DELETE"])
def delete_enrollment(id):
    enrollment = Enrollment.query.get(id)

    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    
    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({'message': 'La matricula del curso se ha eliminado correctamente.'})