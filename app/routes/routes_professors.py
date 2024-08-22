from flask import Blueprint, request, jsonify
from app.models import Professor, ProfessorStudyCenter  
from app.models.course import Course
from app.models.student import Student
from app.models import StudyCenter
from app.models import User, UserRol, Rol
from app.models.professor_student import ProfessorStudent
from app.schema.professor_schema import ProfessorSchema, ProfessorBasicSchema
from app.schema.course_schema import CourseSchema
from app.schema.student_schema import StudentSchema
from app.schema.studycenter_schema import StudyCenterSchema

from app.config import Config
from app.utils.token_manager import decode_token, encode_token

from app import db

# Definir el blueprint para las rutas de Professor
bp = Blueprint('professors', __name__)

professor_schema = ProfessorSchema()
professors_schema = ProfessorSchema(many=True)
professor_basic_schema = ProfessorBasicSchema()
professors_basic_schema = ProfessorBasicSchema(many=True)
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
studyCenter_schema = StudyCenterSchema()
studyCenters_schema = StudyCenterSchema(many=True)

@bp.route('/professor', methods=["POST"])
def add_professor():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    data = request.json

    required_fields = ['professors_name', 'professors_email', 'professors_user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    professors_name = data['professors_name']
    professors_email = data['professors_email']
    professors_user_id = data['professors_user_id']

    existing_professor = Professor.query.filter_by(professors_email=professors_email).first()
    if existing_professor:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_professor =Professor(professors_name=professors_name, professors_email=professors_email, professors_user_id=professors_user_id)
    
    try:
        db.session.add(new_professor)
        db.session.commit()
        professor_rol = Rol.query.get(3)
        if professor_rol is None:
            return jsonify({'error': 'Rol not found'}), 404
        professor_rol_entry = UserRol(user_id=new_professor.professors_user_id, rol_id=professor_rol.rols_id)
        db.session.add(professor_rol_entry) 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el professor', 'details': str(e)}), 500

    professor = Professor.query.get(new_professor.professors_id)
    return professor_schema.jsonify(professor), 201

@bp.route('/professors', methods=["GET"])
def all_professors():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    all_professors = Professor.query.all()
    resul = professors_basic_schema.dump(all_professors)
   
    return jsonify(resul)

@bp.route("/professor/<user_id>", methods=["GET"])
def get_professor(user_id):
    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.filter_by(professors_user_id=user_id).first()

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    result = {
        'professor': {
            'professor_id': professor.professors_id,
            'professor_name': professor.professors_name,
            'professor_email': professor.professors_email
        }
    }

    professor_study_centers = ProfessorStudyCenter.query.filter_by(professor_id=professor.professors_id).all()
    study_center_ids = [psc.studyCenter_id for psc in professor_study_centers]
    study_centers = StudyCenter.query.filter(StudyCenter.studyCenters_id.in_(study_center_ids)).all()

    study_centers_data = studyCenters_schema.dump(study_centers)
    result['study_centers'] = study_centers_data

    return jsonify(result)

# @bp.route("/professor/<id>", methods=["GET"])
# def get_professor(id):

#     auth_header = request.headers.get('Authorization')
#     try:
#         decoded_token = decode_token(auth_header)
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 401

#     professor = Professor.query.get(id)

#     if professor is None:
#         return jsonify({'message': 'Professor not found'}), 404

#     result = professor_schema.dump(professor)

#     professor_students = ProfessorStudent.query.filter_by(professor_student_professor_id=id).all()
#     student_ids = [ps.professor_student_student_id for ps in professor_students]
#     students = Student.query.filter(Student.students_id.in_(student_ids)).all()
#     students_data = students_schema.dump(students)
#     result['students'] = students_data
   
#     courses = Course.query.filter_by(courses_professor_id=id).all()
#     result['courses'] = courses_schema.dump(courses)

#     professor_study_centers = ProfessorStudyCenter.query.filter_by(professor_id=id).all()
#     study_center_ids = [psc.studyCenter_id for psc in professor_study_centers]
#     study_centers = StudyCenter.query.filter(StudyCenter.studyCenters_id.in_(study_center_ids)).all()

#     study_centers_data = studyCenters_schema.dump(study_centers)
#     result['study_centers'] = study_centers_data

#     return jsonify(result)



@bp.route("/professor/<id>", methods=["PUT"])
def update_professor(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    data = request.json
    professor.professors_name = data.get('professors_name', professor.professors_name)
    professor.professors_email = data.get('professors_email', professor.professors_email)
    professor.professors_user_id = data.get('professors_user_id', professor.professors_user_id)

    db.session.commit()

    return professor_schema.jsonify(professor)

@bp.route("/professor/<id>", methods=["DELETE"])
def delete_professor(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    UserRol.query.filter_by(user_id=professor.professors_user_id, rol_id=3).delete()
    db.session.delete(professor)
    db.session.commit()

    return jsonify({'message': 'Professor deleted'})