from flask import Blueprint, request, jsonify
from app import db
from app.models import StudyCenter
from app.models.student import Student
from app.models.course import Course
from app.models.professor import Professor
from app.models.studycenter_student import StudyCenterStudent
from app.models import User, UserRol, Rol
from app.schema.student_schema import StudentSchema
from app.schema.course_schema import CourseSchema
from app.schema.professor_schema import ProfessorBasicSchema
from app.schema.studycenter_schema import StudyCenterSchema, StudyCenterDetailSchema

from app.config import Config
from app.utils.token_manager import decode_token, encode_token

bp = Blueprint('studycenters', __name__)

studyCenter_schema = StudyCenterSchema()
studyCenters_schema = StudyCenterSchema(many=True)
studyCenter_detail_schema = StudyCenterDetailSchema()
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
professor_schema = ProfessorBasicSchema()
professors_schema = ProfessorBasicSchema(many=True)

@bp.route('/studycenter', methods=["POST"])
def add_studycenter():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    data = request.json

    required_fields = ['studyCenters_name', 'studyCenters_email', 'studyCenters_user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    studyCenters_name = data['studyCenters_name']
    studyCenters_email = data['studyCenters_email']
    studyCenters_user_id = data ['studyCenters_user_id']

    existing_user = StudyCenter.query.filter_by(studyCenters_email=studyCenters_email).first()
    if existing_user:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_center =  StudyCenter( 
        studyCenters_name= studyCenters_name, 
        studyCenters_email= studyCenters_email, 
        studyCenters_user_id = studyCenters_user_id
    )
    
    try:
        db.session.add(new_center)
        db.session.commit()
        center_rol = Rol.query.get(4)
        if center_rol is None:
            return jsonify({'error': 'Rol not found'}), 404
        center_rol_entry = UserRol(user_id=new_center.studyCenters_user_id, rol_id=center_rol.rols_id)
        db.session.add(center_rol_entry) 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el centro de estudios', 'details': str(e)}), 500

    center = StudyCenter.query.get(new_center.studyCenters_id)
    return studyCenter_schema.jsonify(center), 201

@bp.route('/studycenters', methods=["GET"])
def all_studycenters():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    all_studycenters = StudyCenter.query.all()
    result = studyCenters_schema.dump(all_studycenters)
    
    return jsonify(result)

@bp.route("/studycenter/<id>", methods=["GET"])
def get_studycenter(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    studyCenter = StudyCenter.query.get(id)

    if studyCenter is None:
        return jsonify({'message': 'StudyCenter not found'}), 404

    result = studyCenter_detail_schema.dump(studyCenter)

    studyCenter_students = StudyCenterStudent.query.filter_by(studycenter_student_center_id=id).all()
    student_ids = [ps.studycenter_student_student_id for ps in studyCenter_students]
    students = Student.query.filter(Student.students_id.in_(student_ids)).all()
    students_data = students_schema.dump(students)
    result['students'] = students_data

    courses = Course.query.filter_by(courses_studycenter_id=id).all()
    result['courses'] = courses_schema.dump(courses)

    professors = Professor.query.join(Course).filter(Course.courses_studycenter_id == id).all()
    result['professors'] = professors_schema.dump(professors)

    return jsonify(result)


@bp.route("/studycenter/<id>", methods=["PUT"])
def update_studycenter(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    studyCenter = StudyCenter.query.get(id)

    if studyCenter is None:
        return jsonify({'message': 'StudyCenter not found'}), 404

    data = request.json
    studyCenter.studyCenters_name = data.get('studyCenters_name', studyCenter.studyCenters_name)
    studyCenter.studyCenters_email = data.get('studyCenters_email', studyCenter.studyCenters_email)
 
    db.session.commit()

    return studyCenter_schema.jsonify(studyCenter)

@bp.route("/studycenter/<id>", methods=["DELETE"])
def delete_studycenter(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    studyCenter = StudyCenter.query.get(id)

    if studyCenter is None:
        return jsonify({'message': 'StudyCenter not found'}), 404
    
    UserRol.query.filter_by(user_id=studyCenter.studyCenters_user_id, rol_id=4).delete()
    db.session.delete(studyCenter)
    db.session.commit()

    return jsonify({'message': 'StudyCenter deleted'})