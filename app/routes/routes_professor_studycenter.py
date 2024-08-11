from flask import Blueprint, request, jsonify
from app.models import Professor, StudyCenter, ProfessorStudyCenter
from app.schema.professor_studycenter_schema import ProfessorStudyCenterSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token

from app import db

bp = Blueprint('professor_studycenter', __name__)

professor_studycenter_schema = ProfessorStudyCenterSchema()
professor_studycenters_schema = ProfessorStudyCenterSchema(many=True)

@bp.route('/professor_studycenter', methods=["POST"])
def add_professor_studycenter():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    data = request.json

    required_fields = ['professor_id', 'studyCenter_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Field {field} is required'}), 400

    professor_id = data['professor_id']
    studyCenter_id = data['studyCenter_id']

    # Verificar existencia de los IDs
    professor = Professor.query.get(professor_id)
    studyCenter = StudyCenter.query.get(studyCenter_id)

    if not professor:
        return jsonify({'error': 'Professor not found'}), 404

    if not studyCenter:
        return jsonify({'error': 'StudyCenter not found'}), 404

    # Verificar si ya existe la relación
    existing_relationship = ProfessorStudyCenter.query.filter_by(
        professor_id=professor_id, studyCenter_id=studyCenter_id).first()
    if existing_relationship:
        return jsonify({'error': 'The relationship already exists'}), 400

    # Crear una nueva relación
    new_relationship = ProfessorStudyCenter(
        professor_id=professor_id, studyCenter_id=studyCenter_id)

    try:
        db.session.add(new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Relationship could not be added', 'details': str(e)}), 500

    return jsonify({'message': 'Successfully Added Relationship'}), 201

@bp.route('/professor_studycenters', methods=["GET"])
def all_professor_studycenters():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    all_professor_studycenters = ProfessorStudyCenter.query.all()
    result = professor_studycenters_schema.dump(all_professor_studycenters)
    return jsonify(result)

@bp.route('/professor_studycenter', methods=["DELETE"])
def delete_professor_studycenter():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    data = request.json

    required_fields = ['professor_id', 'studyCenter_id']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    professor_id = data['professor_id']
    studyCenter_id = data['studyCenter_id']

    relationship = ProfessorStudyCenter.query.filter_by(professor_id=professor_id, studyCenter_id=studyCenter_id).first()

    if not relationship:
        return jsonify({'error': 'Relationship not found'}), 404

    try:
        db.session.delete(relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Could not eliminate the relationship', 'details': str(e)}), 500
    
    return jsonify({'message': 'Relationship successfully eliminated'}), 200