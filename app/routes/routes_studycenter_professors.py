from flask import Blueprint, request, jsonify
from app import db
from app.models import StudyCenterProfessor, StudyCenterProfessorSchema

bp = Blueprint('studycenter_professors', __name__)

@bp.route('/studycenter_professors', methods=['GET'])
def get_all_studycenter_professors():
    studycenter_professors = StudyCenterProfessor.query.all()
    schema = StudyCenterProfessorSchema(many=True)
    result = schema.dump(studycenter_professors)
    return jsonify(result)

@bp.route('/studycenter_professors', methods=['POST'])
def create_studycenter_professor():
    data = request.get_json()
    # Asegúrate de que los datos tienen los campos necesarios
    if 'studycenter_id' not in data or 'professor_id' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Crea la instancia del modelo con los datos proporcionados
    schema = StudyCenterProfessorSchema()
    try:
        studycenter_professor = schema.load(data, session=db.session)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    db.session.add(studycenter_professor)
    db.session.commit()
    result = schema.dump(studycenter_professor)
    return jsonify(result), 201

@bp.route('/studycenter_professors/<int:studycenter_id>/<int:professor_id>', methods=['DELETE'])
def delete_studycenter_professor(studycenter_id, professor_id):
    studycenter_professor = StudyCenterProfessor.query.get((studycenter_id, professor_id))
    if studycenter_professor is None:
        return jsonify({'message': 'Not found'}), 404
    
    db.session.delete(studycenter_professor)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200