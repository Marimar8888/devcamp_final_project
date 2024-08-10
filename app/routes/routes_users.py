from app import db
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from app.models import User, UserRol, Rol
from app.schema.user_schema import UserSchema
from app.config import Config

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

    hashed_password = bcrypt.hashpw(users_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    existing_user = User.query.filter_by(users_email=users_email).first()
    if existing_user:
        return jsonify({'error': 'El email ya está en uso'}), 400

    new_user = User(users_name=users_name, users_email=users_email, users_password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        user_role = Rol.query.get(1)
        if user_role is None:
            return jsonify({'error': 'Role not found'}), 404
        user_role_entry = UserRol(user_id=new_user.users_id, rol_id=user_role.rols_id)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el usuario', 'details': str(e)}), 500

    user = User.query.get(new_user.users_id)

    return jsonify(user_schema.dump(user)), 201

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

    user_roles = UserRol.query.filter_by(user_id=id).all()
    rols = [Rol.query.get(user_rol.rol_id) for user_rol in user_roles]

    user_data = user_schema.dump(user)
    user_data['rols'] = [{'rols_id': rol.rols_id, 'rols_name': rol.rols_name} for rol in rols]

    return jsonify(user_data)

@bp.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.users_name = data.get('users_name', user.users_name)
    user.users_email = data.get('users_email', user.users_email)
    if 'users_password' in data:
        user.users_password = bcrypt.hashpw(data['users_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db.session.commit()

    return jsonify(user_schema.dump(user))

@bp.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'})

@bp.route('/login', methods=["POST"])
def login():
    data = request.json

    required_fields = ['users_email', 'users_password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Field {field} is required'}), 400

    users_email = data['users_email']
    users_password = data['users_password']

    user = User.query.filter_by(users_email=users_email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.checkpw(users_password.encode('utf-8'), user.users_password.encode('utf-8')):
        return jsonify({'error': 'Incorrect password'}), 401
    
    token_payload = {
        'users_id': user.users_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')

    return jsonify({'message': 'Login successful', 'token':token}), 200