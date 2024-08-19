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
    current_app.logger.info("Iniciando proceso de agregar curso")
    
    # Verificar el tipo de contenido del request
    if 'multipart/form-data' not in request.content_type:
        return jsonify({'error': 'Unsupported Media Type'}), 415

    # Log de todos los archivos y campos recibidos
    current_app.logger.info(f"Archivos recibidos: {request.files}")
    current_app.logger.info(f"Form recibido: {request.form}")

    # Obtener el archivo (imagen) del formulario
    courses_image_file = request.files.get('file')
    current_app.logger.info(f"Archivo recibido: {courses_image_file.filename if courses_image_file else 'No se recibió archivo'}")

    # Obtener los datos del formulario
    courses_title = request.form.get('courses_title')
    courses_content = request.form.get('courses_content')
    courses_price = request.form.get('courses_price')
    courses_discounted_price = request.form.get('courses_discounted_price')
    courses_professor_id = request.form.get('courses_professor_id')
    courses_studycenter_id = request.form.get('courses_studycenter_id')
    courses_category_id = request.form.get('courses_category_id')

    # Procesar el archivo de imagen
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if courses_image_file and courses_image_file.filename:
        current_app.logger.info("Procesando la imagen para guardar")
        # Guardar la imagen en el servidor usando la función save_file
        filename, error = save_file(courses_image_file, upload_folder)

        if error:
            current_app.logger.error(f"Error al guardar el archivo: {error}")
            return jsonify({'error': error}), 400
        
        current_app.logger.info(f"Archivo guardado como: {filename}")
        # Crear la URL relativa para almacenar en la base de datos
        # file_url = os.path.join('static/uploads', filename)  # **Cambio: Crear URL relativa para la imagen en lugar de datos binarios**
        file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
    else:
        file_url = None  # Si no hay imagen, asigna None

    # Verificar que todos los campos obligatorios estén presentes
    if not courses_title or not courses_price or not courses_professor_id or not courses_category_id:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    # Procesar el curso y guardar en la base de datos
    new_course = Course(
        courses_title=courses_title,
        courses_content=courses_content,
        courses_image=file_url,  # **Cambio: Guardar la URL de la imagen en lugar de los datos binarios**
        courses_price=courses_price,
        courses_discounted_price=courses_discounted_price,
        courses_professor_id=courses_professor_id,
        courses_studycenter_id=courses_studycenter_id,
        courses_category_id=courses_category_id
    )

    db.session.add(new_course)
    db.session.commit()
    current_app.logger.info(f"Curso guardado con ID: {new_course.courses_id}")
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