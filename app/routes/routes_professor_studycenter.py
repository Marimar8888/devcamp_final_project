from flask import Blueprint, request, jsonify
from app.models import Professor, StudyCenter, ProfessorStudyCenter
from app.schema.professor_studycenter_schema import ProfessorStudyCenterSchema

from app import db

bp = Blueprint('professor_studycenter', __name__)

professor_studycenter_schema = ProfessorStudyCenterSchema()
professor_studycenters_schema = ProfessorStudyCenterSchema(many=True)

@bp.route('/professor_studycenter', methods=["POST"])
def add_professor_studycenter():
    data = request.json

    required_fields = ['professor_id', 'studyCenter_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

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
        return jsonify({'error': 'La relación ya existe'}), 400

    # Crear una nueva relación
    new_relationship = ProfessorStudyCenter(
        professor_id=professor_id, studyCenter_id=studyCenter_id)

    try:
        db.session.add(new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar la relación', 'details': str(e)}), 500

    return jsonify({'message': 'Relación agregada exitosamente'}), 201

@bp.route('/professor_studycenters', methods=["GET"])
def all_professor_studycenters():
    all_professor_studycenters = ProfessorStudyCenter.query.all()
    print(f"Retrieved records: {all_professor_studycenters}")
    result = professor_studycenters_schema.dump(all_professor_studycenters)
    print(f"Serialized result: {result}")  # Imprime el resultado serializado
    return jsonify(result)

@bp.route('/professor_studycenter', methods=["DELETE"])
def delete_professor_studycenter():
    data = request.json

    required_fields = ['professor_id', 'studyCenter_id']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400
    
    professor_id = data['professor_id']
    studyCenter_id = data['studyCenter_id']

    relationship = ProfessorStudyCenter.query.filter_by(professor_id=professor_id, studyCenter_id=studyCenter_id).first()

    if not relationship:
        return jsonify({'error': 'Relación no encontrada'}), 404

    try:
        db.session.delete(relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo eliminar la relación', 'details': str(e)}), 500
    
    return jsonify({'message': 'Relación eliminada exitosamente'}), 200