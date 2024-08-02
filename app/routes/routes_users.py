from flask import Blueprint, request, jsonify
from app.models import User, UserSchema
from app import db

# Definir el blueprint para las rutas de User
bp = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route('', methods=["POST"])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    new_user = User(name, email, password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

@bp.route('', methods=["GET"])
def all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    
    return jsonify(result)

@bp.route("/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)

    return user_schema.jsonify(user)