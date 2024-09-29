from flask import Blueprint, request, jsonify
from app.models import Category 
from app.schema.category_schema import CategorySchema, CategoryBasicSchema
from app import db
from app.config import Config
from app.utils.token_manager import decode_token, encode_token

bp = Blueprint('categories', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
categories_basic_schema = CategoryBasicSchema(many=True)

@bp.route('/category', methods=["POST"])
def add_category():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    data = request.json

    required_fields = ['categories_name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    categories_name = data['categories_name']

    existing_category = Category.query.filter_by(categories_name = categories_name).first()
    if existing_category:
        return jsonify({'error': 'The category already exists'}), 400
    
    new_category = Category(categories_name=categories_name)

    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Unable to add category'})
    
    category = Category.query.get(new_category.categories_id)

    return jsonify(category_schema.dump(category)), 201

@bp.route('/categories', methods=['GET'])
def all_categories():

    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)

    return jsonify(result)

@bp.route('/category_names', methods=['GET'])
def all_categories_names():

    all_categories = Category.query.all()
    result = categories_basic_schema.dump(all_categories)

    return jsonify(result)


@bp.route('/category/<id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)

    if category is None:
        return jsonify({'message': 'Category not found'}), 404
    
    return category_schema.jsonify(category)

@bp.route('/category/<id>', methods=['PUT'])
def update_category(id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    category = Category.query.get(id)

    if category is None:
        return jsonify({'error:': 'Category not found'}), 404
    
    data = request.json

    category.categories_name = data.get('categories_name', category.categories_name)

    db.session.commit()

    return category_schema.jsonify(category)



    