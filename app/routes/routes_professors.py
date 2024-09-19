from flask import Blueprint, request, jsonify
from app.models import Professor, ProfessorStudyCenter  
from app.models.course import Course
from app.models.student import Student
from app.models import StudyCenter
from app.models import User, UserRol, Rol
from app.models import Enrollment
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

    data = request.form

    required_fields = [
        'professors_first_name', 'professors_last_name', 'professors_email', 'professors_user_id', 'professors_dni', 'professors_address', 
        'professors_city', 'professors_postal', 'professors_number_card', 'professors_exp_date', 'professors_cvc'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    professors_first_name = data['professors_first_name']
    professors_last_name = data['professors_last_name']
    professors_email = data['professors_email']
    professors_user_id = data['professors_user_id']
    professors_dni = data['professors_dni']
    professors_address = data['professors_address']
    professors_city = data['professors_city']
    professors_postal = data['professors_postal']
    professors_number_card = data['professors_number_card']
    professors_exp_date = data['professors_exp_date']
    professors_cvc = data['professors_cvc']

    existing_professor = Professor.query.filter_by(professors_email=professors_email).first()
    if existing_professor:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_professor =Professor(
        professors_first_name=professors_first_name, 
        professors_last_name=professors_last_name, 
        professors_email=professors_email, 
        professors_user_id=professors_user_id,
        professors_dni = professors_dni, 
        professors_address = professors_address, 
        professors_city = professors_city,
        professors_postal = professors_postal, 
        professors_number_card = professors_number_card, 
        professors_exp_date = professors_exp_date,
        professors_cvc = professors_cvc
    )
    
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

@bp.route("/professor/user_id/<user_id>", methods=["GET"])
def get_professor_id_by_user_id(user_id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.filter_by(professors_user_id=user_id).first()

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    return jsonify({'professors_id': professor.professors_id})

@bp.route("/professor/userId/<user_id>", methods=["GET"])
def get_professor_by_user_id(user_id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.filter_by(professors_user_id=user_id).first()

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    return jsonify(professor_schema.dump(professor))

@bp.route("/professor/<id>", methods=["GET"])
def get_professor(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    result = professor_basic_schema.dump(professor)

    return jsonify(result)

@bp.route("/professor/all_dates/<professorId>", methods=["GET"])
def get_all_dates_professor(professorId):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.get(professorId)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    professor_schema = {
        'professor': { 
            'professors_id': professor.professors_id,
            'professors_first_name': professor.professors_first_name,
            'professors_last_name': professor.professors_last_name,
            'professors_email': professor.professors_email,
            'professors_user_id': professor.professors_user_id,
            'professors_dni': professor.professors_dni,
            'professors_address': professor.professors_address,
            'professors_city': professor.professors_city,
            'professors_postal': professor.professors_postal,
            'professors_number_card': professor.professors_number_card,
            'professors_exp_date': professor.professors_exp_date,
            'professors_cvc': professor.professors_cvc
        }
    }

    result = professor_schema

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    paginated_courses = Course.query.filter_by(courses_professor_id=professorId).paginate(page=page, per_page=limit, error_out=False)
    courses_data = courses_schema.dump(paginated_courses.items)

    result['courses'] = {
        'items': courses_data,
        'total': paginated_courses.total,
        'page': page,
        'pages': paginated_courses.pages
    }

    # Students of a teacher 
    students = db.session.query(Student).\
        join(Enrollment, Student.students_id == Enrollment.enrollments_student_id).\
        join(Course, Enrollment.enrollments_course_id == Course.courses_id).\
        filter(Course.courses_professor_id == professorId).all()
    students_data = students_schema.dump(students)
    result['students'] = students_data
  
    # Centers for which the teacher works
    professor_study_centers = ProfessorStudyCenter.query.filter_by(professor_id=professorId).all()
    study_center_ids = [psc.studyCenter_id for psc in professor_study_centers]
    study_centers = StudyCenter.query.filter(StudyCenter.studyCenters_id.in_(study_center_ids)).all()
    study_centers_data = studyCenters_schema.dump(study_centers)
    result['study_centers'] = study_centers_data

    return jsonify(result)

@bp.route("/professor/<id>", methods=["PATCH"])
def update_professor(id):

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    data = request.form
    if 'professors_first_name' in data:
        professor.professors_first_name = data['professors_first_name']
    if 'professors_last_name' in data:
        professor.professors_last_name = data['professors_last_name']
    if 'professors_email' in data:
        professor.professors_email = data['professors_email']
    if 'professors_user_id' in data:
        professor.professors_user_id = data['professors_user_id']
    if 'professors_dni' in data:    
        professor.professors_dni = data['professors_dni']
    if 'professors_address' in data:
        professor.professors_address = data['professors_address']
    if 'professors_city' in data:
        professor.professors_city = data['professors_city']
    if 'professors_postal' in data:
        professor.professors_postal = data['professors_postal']
    if 'professors_number_card' in data:
        professor.professors_number_card = data['professors_number_card']
    if 'professors_exp_date' in data:
        professor.professors_exp_date = data['professors_exp_date']
    if 'professors_cvc' in data:
        professor.professors_cvc = data['professors_cvc']

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

