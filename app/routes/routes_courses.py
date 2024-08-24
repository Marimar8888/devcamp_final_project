import base64
from flask import Blueprint, request, jsonify, current_app, url_for
from app import db
import os

from app.models import Course, CourseSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token
from app.utils import save_file


bp = Blueprint('courses', __name__)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

@bp.route('/course', methods=["POST"])
def add_course():    
    if 'multipart/form-data' not in request.content_type:
        return jsonify({'error': 'Unsupported Media Type'}), 415

    courses_image_file = request.files.get('file')

    courses_title = request.form.get('courses_title')
    courses_content = request.form.get('courses_content')
    courses_price = request.form.get('courses_price')
    courses_discounted_price = request.form.get('courses_discounted_price')
    courses_professor_id = request.form.get('courses_professor_id')
    courses_studycenter_id = request.form.get('courses_studycenter_id')
    courses_category_id = request.form.get('courses_category_id')

    upload_folder = current_app.config['UPLOAD_FOLDER']
    if courses_image_file and courses_image_file.filename:
        filename, error = save_file(courses_image_file, upload_folder)

        if error:
            return jsonify({'error': error}), 400
         
        file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
    else:
        file_url = None  

    if not courses_title or not courses_price or not courses_professor_id or not courses_category_id:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    new_course = Course(
        courses_title=courses_title,
        courses_content=courses_content,
        courses_image=file_url,  
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

@bp.route("/store/courses/<categoryId>", methods=["GET"])
def get_courses_by_category(categoryId):
    courses = Course.query.filter_by(courses_category_id=categoryId).all()

    if not courses:
        return jsonify({'message': 'Courses not found'}), 404

    return course_schema.jsonify(courses, many=True)

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

    if 'courses_image' in data:
        if data['courses_image'] is None and course.courses_image:
            try:
                image_filename = os.path.basename(course.courses_image)
                image_path = os.path.join('app', 'static', 'uploads', image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)
                else:
                    print("El archivo no existe en la ruta especificada.")  
            except Exception as e:
                return jsonify({'error': 'Failed to delete the image file', 'details': str(e)}), 500

        course.courses_image = data['courses_image']

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
    
    image_path = None
    if course.courses_image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(course.courses_image))
    
    db.session.delete(course)
    db.session.commit()

    if image_path and os.path.exists(image_path):
        os.remove(image_path)

    response = jsonify({'message': 'Course deleted'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return jsonify({'message': 'Course deleted'})