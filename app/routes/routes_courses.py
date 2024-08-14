from flask import Blueprint, request, jsonify
from app.models import Course, CourseSchema
from app import db
from app.config import Config
from app.utils.token_manager import decode_token, encode_token

bp = Blueprint('courses', __name__)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

@bp.route('/course', methods=["POST"])
def add_course():

    auth_header = request.headers.get('Authorization')
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    data = request.json
   
    courses_title = data.get('courses_title')
    courses_content = data.get('courses_content')
    courses_image = data.get('courses_image')
    courses_price = data.get('courses_price')
    courses_discounted_price = data.get('courses_discounted_price')
    courses_professor_id = data.get('courses_professor_id')
    courses_studycenter_id = data.get('courses_studycenter_id')
    courses_category_id = data.get('courses_category_id')
 
    if courses_title is None or courses_price is None:
        return jsonify({'error': 'Faltan campos obligatorios en el JSON'}), 400

    # Crea un nuevo curso con campos opcionales que pueden ser None
    new_course = Course(
        courses_title=courses_title,
        courses_content=courses_content,
        courses_image=courses_image,
        courses_price=courses_price,
        courses_discounted_price=courses_discounted_price,
        courses_professor_id=courses_professor_id,
        courses_studycenter_id=courses_studycenter_id,
        courses_category_id=courses_category_id
    )

    db.session.add(new_course)
    db.session.commit()

    course = Course.query.get(new_course.courses_id)

    return course_schema.jsonify(course)

@bp.route('/courses', methods=["GET"])
def all_courses():
    all_courses = Course.query.all()
    result = courses_schema.dump(all_courses)
    
    return jsonify(result)

@bp.route("/course/<id>", methods=["GET"])
def get_course(id):
    course = Course.query.get(id)

    if course is None:
        return jsonify({'message': 'Course not found'}), 404

    return course_schema.jsonify(course)

@bp.route("/course/<id>", methods=["PUT"])
def update_course(id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    course = Course.query.get(id)

    if course is None:
         return jsonify({'message': 'Course not found'}), 404
    
    data = request.json
    course.courses_title = data.get('courses_title', course.courses_title)
    course.courses_content = data.get('courses_content',  course.courses_content)
    course.courses_image = data.get('courses_image', course.courses_image)
    course.courses_price = data.get('courses_price', course.courses_price)
    course.courses_discounted_price = data.get('courses_discounted_price', course.courses_discounted_price)
    course.courses_professor_id = data.get('courses_professor_id', course.courses_professor_id)
    course.courses_studycenter_id = data.get('courses_studycenter_id', course.courses_studycenter_id)
    course.courses_category_id = data.get('courses_category_id', course.courses_category_id)

    db.session.commit()

    return course_schema.jsonify(course)

@bp.route("/course/<id>", methods=["PATCH"])
def updatePatch_course(id):

    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    course = Course.query.get(id)

    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    
    data = request.json

    if 'courses_title' in data:
        course.courses_title = data['courses_title']
    if 'courses_content' in data:
        course.courses_content = data['courses_content']
    if 'courses_image' in data:
        course.courses_image = data['courses_image']
    if 'courses_price' in data:
        course.courses_price = data['courses_price']
    if 'courses_discounted_price' in data:
        course.courses_discounted_price = data['courses_discounted_price']
    if 'courses_professor_id' in data:
        course.courses_professor_id = data['courses_professor_id']
    if 'courses_studycenter_id' in data:
        course.courses_studycenter_id = data['courses_studycenter_id']
    if 'courses_category_id' in data:
        course.courses_category_id = data['courses_category_id']

    db.session.commit()

    return course_schema.jsonify(course)

@bp.route("/course/<id>", methods=["DELETE"])
def delete_course(id):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
        
    course = Course.query.get(id)

    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    
    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted'})