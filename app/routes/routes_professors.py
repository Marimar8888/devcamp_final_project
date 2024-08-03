from flask import Blueprint, request, jsonify
from app.models import Professor, ProfessorSchema
from app import db

# Definir el blueprint para las rutas de Professor
bp = Blueprint('professors', __name__)

professor_schema = ProfessorSchema()
professors_schema = ProfessorSchema(many=True)

@bp.route('/professor', methods=["POST"])
def add_professor():
    data = request.json

    required_fields = ['professors_name', 'professors_email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    professors_name = data['professors_name']
    professors_email = data['professors_email']
 
    existing_professor = Professor.query.filter_by(professors_email=professors_email).first()
    if existing_professor:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_professor =Professor(professors_name=professors_name, professors_email=professors_email)
    
    try:
        db.session.add(new_professor)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el usuario', 'details': str(e)}), 500

    professor = Professor.query.get(new_professor.professors_id)
    return professor_schema.jsonify(professor), 201

@bp.route('/professors', methods=["GET"])
def all_professors():
    all_professors = Professor.query.all()
    result = professors_schema.dump(all_professors)
    
    return jsonify(result)

@bp.route("/professor/<id>", methods=["GET"])
def get_professor(id):
    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    return professor_schema.jsonify(professor)

@bp.route("/professor/<id>", methods=["PUT"])
def update_professor(id):
    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    data = request.json
    professor.professors_name = data.get('professors_name', professor.professors_name)
    professor.professors_email = data.get('professors_email', professor.professors_email)
    
    db.session.commit()

    return professor_schema.jsonify(professor)

@bp.route("/professor/<id>", methods=["DELETE"])
def delete_professor(id):
    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({'message': 'Professor not found'}), 404

    db.session.delete(professor)
    db.session.commit()

    return jsonify({'message': 'Professor deleted'})