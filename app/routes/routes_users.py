from app import db
import bcrypt
from flask import Blueprint, request, jsonify
from app.models import User, UserRol, Rol
from app.schema.user_schema import UserSchema
from app.config import Config
from app.utils import decode_token, encode_token

# Definir el blueprint para las rutas de User
bp = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route('/user', methods=["POST"])
def add_user():

    data = request.json

    required_fields = ['users_name', 'users_email', 'users_password']
    for field in required_fields:
        if field not in data or not data[field]:
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
        user_rol = Rol.query.get(1)
        if user_rol is None:
            return jsonify({'error': 'Rol not found'}), 404
        user_rol_entry = UserRol(user_id=new_user.users_id, rol_id=user_rol.rols_id)
        db.session.add(user_rol_entry) 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'CUnable to add user', 'details': str(e)}), 500

    user = User.query.get(new_user.users_id)

    return jsonify(user_schema.dump(user)), 201

@bp.route('/users', methods=["GET"])
def all_users():
    
    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    all_users = User.query.all()
    result = users_schema.dump(all_users)
    
    return jsonify(result)

@bp.route("/user/<id>", methods=["GET"])
def get_user(id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

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

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

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
    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    roles_count = UserRol.query.filter_by(user_id=id).count()
    if roles_count > 1:
        return jsonify({'error': 'User cannot be deleted because it has associated roles'}), 400

    UserRol.query.filter_by(user_id=user.users_id, rol_id=1).delete()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'})

@bp.route('/login', methods=["POST"])
def login():
    data = request.json

    required_fields = ['users_email', 'users_password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Field {field} is required'}), 400

    users_email = data['users_email']
    users_password = data['users_password']

    user = User.query.filter_by(users_email=users_email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.checkpw(users_password.encode('utf-8'), user.users_password.encode('utf-8')):
        return jsonify({'error': 'Incorrect password'}), 401
    
    token = encode_token(user.users_id)
    user_name = user.users_name
    

    return jsonify({'message': 'Login successful', 'token':token, 'user_name':user_name}), 200