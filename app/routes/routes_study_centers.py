from flask import Blueprint, request, jsonify
from app.models import StudyCenter, StudyCenterSchema
from app import db

# Definir el blueprint para las rutas de User
bp = Blueprint('studycenters', __name__)

studyCenter_schema = StudyCenterSchema()
studyCenters_schema = StudyCenterSchema(many=True)

@bp.route('/studycenter', methods=["POST"])
def add_user():
    data = request.json

    required_fields = ['studyCenters_name', 'studyCenters_professor_id', 'studyCenters_email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    studyCenters_name = data['studyCenters_name']
    studyCenters_professor_id = data['studyCenters_professor_id']
    studyCenters_email = data['studyCenters_email']

    existing_user = StudyCenter.query.filter_by(studyCenters_email=studyCenters_email).first()
    if existing_user:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_center =  StudyCenter( studyCenters_name= studyCenters_name, studyCenters_professor_id=studyCenters_professor_id, studyCenters_emaill= studyCenters_email)
    
    try:
        db.session.add(new_center)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el centro de estudios', 'details': str(e)}), 500

    center = User.query.get(new_center. studyCenters_id)
    return studyCenter_schema.jsonify(center), 201

@bp.route('/users', methods=["GET"])
def all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    
    return jsonify(result)

@bp.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return user_schema.jsonify(user)

@bp.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.users_name = data.get('users_name', user.users_name)
    user.users_email = data.get('users_email', user.users_email)
    user.users_password = data.get('users_password', user.users_password)

    db.session.commit()

    return user_schema.jsonify(user)

@bp.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'})