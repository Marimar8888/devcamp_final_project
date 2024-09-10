from flask import Blueprint, request, jsonify
from app.models import Course, User, Favorite
from app.schema.favorite_schema import FavoriteSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token

from app import db

bp = Blueprint('favorites', __name__)

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)

@bp.route('/favorite', methods=['POST'])
def add_favorite():

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    data = request.json

    required_fields = ['favorites_user_id', 'favorites_course_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    favorites_user_id = data['favorites_user_id']
    favorites_course_id = data['favorites_course_id']

    user = User.query.get(favorites_user_id)
    course = Course.query.get(favorites_course_id)

    if not user:
        return jsonify({'error': f'User with ID {favorites_user_id} not found'}), 404
    
    if not course:
        return jsonify({'error': f'Course with ID {favorites_course_id} not found'}), 404
    
    existing_relationship = Favorite.query.filter_by(
        favorites_user_id = favorites_user_id,
        favorites_course_id = favorites_course_id
    ).first()

    if existing_relationship:
        return jsonify({'error': 'The relationship already exists'}), 400
    
    new_relationship = Favorite(
        favorites_user_id = favorites_user_id,
        favorites_course_id = favorites_course_id
    )

    try:
        db.session.add(new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Unable to create the relationship', 'details': str(e)}), 500
    
    return jsonify({'message': 'Successfully created relationship'}), 201

@bp.route('/favorites/<user_id>', methods=['GET'])
def get_favorites_by_user_id(user_id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    favorites = Favorite.query.filter_by(favorites_user_id=user_id).all()

    if not favorites:
        return jsonify({'message': 'Favorites not found'}), 404
    
    serialized_data = favorites_schema.dump(favorites)
    print(f"Datos serializados: {serialized_data}")

    return jsonify(serialized_data), 200

@bp.route('/favorite/<int:user_id>/<int:course_id>', methods=['DELETE'])
def delete_favorite_by_user_id(user_id, course_id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    favorite = Favorite.query.filter_by(favorites_user_id=user_id, favorites_course_id=course_id).first()

    if not favorite:
        return jsonify({'message': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite deleted successfully'}), 200