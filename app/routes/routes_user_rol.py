from flask import Blueprint, request, jsonify
from app.models import User, Rol, UserRol
from app.schema.user_rol_schema import UserRolSchema

from app import db

bp = Blueprint('user_rol', __name__)

user_rol_schema = UserRolSchema()
user_rols_schema = UserRolSchema(many=True)

@bp.route('/user_rol', methods=["POST"])
def add_user_rol():
    data = request.json

    required_fields = ['user_id', 'rol_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    user_id = data['user_id']
    rol_id = data['rol_id']

    # Verificar existencia de los IDs
    user = User.query.get(user_id)
    rol = Rol.query.get(rol_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not rol:
        return jsonify({'error': 'Rol not found'}), 404

    # Verificar si ya existe la relación
    existing_relationship = UserRol.query.filter_by(
        user_id=user_id,rol_id=rol_id).first()
    if existing_relationship:
        return jsonify({'error': 'La relación ya existe'}), 400

       # Crear una nueva relación
    new_relationship = UserRol(
         user_id=user_id,rol_id=rol_id)

    try:
        db.session.add(new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el nuevo rol', 'details': str(e)}), 500

    return jsonify({'message': 'El nuevo rol ha sido agregado exitosamente'}), 201

@bp.route('/user_rols', methods=["GET"])
def all_user_rols():
    all_user_rols = UserRol.query.all()
    result = user_rols_schema.dump(all_user_rols)
    return jsonify(result)

@bp.route('/user_rol', methods=["DELETE"])
def delete_user_rol():
    data=request.json

    required_fields = ['user_id', 'rol_id']

    for field in required_fields:
        if field not in data:
            return jsonify({'error:', f'Campo {field} es obligatorio'}), 400
    
    user_id = data['user_id']
    rol_id = data['rol_id']

    relationship = UserRol.query.filter_by(user_id=user_id, rol_id=rol_id).first()

    if not relationship:
        return jsonify({'error': 'No existe dicho rol para el usuario seleccionado'}), 404
    
    try: 
        db.session.delete(relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se puede eliminar el rol', 'details': str(e)}), 500
    
    return jsonify({'message': 'El rol ha sido eliminado con éxito'}), 200