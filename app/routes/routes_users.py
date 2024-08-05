from flask import Blueprint, request, jsonify
from app.models import User
from app.schema.user_schema import UserSchema
from app import db

# Definir el blueprint para las rutas de User
bp = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route('/user', methods=["POST"])
def add_user():
    
    data = request.json

    required_fields = ['users_name', 'users_email', 'users_password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    users_name = data['users_name']
    users_email = data['users_email']
    users_password = data['users_password']

    existing_user = User.query.filter_by(users_email=users_email).first()
    if existing_user:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_user = User(users_name=users_name, users_email=users_email, users_password=users_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el usuario', 'details': str(e)}), 500

    user = User.query.get(new_user.users_id)
    return user_schema.jsonify(user), 201

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