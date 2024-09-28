import base64
from flask import Blueprint, request, jsonify, current_app, url_for
from app import db
import os

from app.models import Course, Enrollment, Favorite
from app.schema.course_schema import CourseSchema, CourseBasicSchema
from app.config import Config
from app.utils.token_manager import decode_token, encode_token, get_user_id_from_token
from app.utils import save_file, delete_course_image


bp = Blueprint('courses', __name__)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
courses_basic_schema = CourseBasicSchema(many=True)

@bp.route('/course', methods=["POST"])
def add_course():    
    if 'multipart/form-data' not in request.content_type:
        return jsonify({'error': 'Unsupported Media Type'}), 415

    courses_image_file = request.files.get('file')
    if courses_image_file:
        print(f"Archivo recibido: {courses_image_file.filename}")  # Muestra el nombre del archivo para verificar
    else:
        print("No se recibió ningún archivo para courses_image")

    courses_title = request.form.get('courses_title')
    courses_content = request.form.get('courses_content')
    courses_price = request.form.get('courses_price')
    courses_discounted_price = request.form.get('courses_discounted_price')
    courses_professor_id = request.form.get('courses_professor_id')
    courses_studycenter_id = request.form.get('courses_studycenter_id')
    courses_category_id = request.form.get('courses_category_id')
    courses_active = request.form.get('courses_active')

    if courses_active is not None:
        courses_active = courses_active.lower() == 'true'

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
        courses_price=float(courses_price),  
        courses_discounted_price=float(courses_discounted_price) if courses_discounted_price else None,
        courses_professor_id=int(courses_professor_id),  
        courses_studycenter_id=int(courses_studycenter_id) if courses_studycenter_id else None,
        courses_category_id=int(courses_category_id),
        courses_active = courses_active
    )

    db.session.add(new_course)
    db.session.commit()
    course = Course.query.get(new_course.courses_id)
    return course_schema.jsonify(course)


@bp.route('/courses', methods=["GET"])
def all_courses():
    page = request.args.get('page', 1, type=int)  
    limit = request.args.get('limit', 10, type=int)  

    paginated_courses = Course.query.paginate(page=page, per_page=limit, error_out=False)

    result = courses_schema.dump(paginated_courses.items)  
    
    return jsonify({
        'courses': result,
        'total': paginated_courses.total,  
        'page': page,
        'pages': paginated_courses.pages 
    })

@bp.route("/course/<id>", methods=["GET"])
def get_course(id):
    course = Course.query.get(id)

    if course is None:
        return jsonify({'message': 'Course not found'}), 404

    return course_schema.jsonify(course)

@bp.route("/store/courses/<categoryId>", methods=["GET"])
def get_courses_by_category(categoryId):
    page = request.args.get('page', 1, type=int)  
    limit = request.args.get('limit', 10, type=int)  

    paginated_courses = Course.query.filter_by(courses_category_id=categoryId).paginate(
        page=page, per_page=limit, error_out=False
    )
    if not paginated_courses:
         return jsonify({'message': 'Courses not found'}), 404

    result = courses_schema.dump(paginated_courses.items)

    return jsonify({
        'courses': result,  
        'total': paginated_courses.total, 
        'page': page,  
        'pages': paginated_courses.pages  
    })

@bp.route("/courses/professor/<int:professorId>/type/<int:TypeId>", methods=["GET"])
def get_courses_professor_by_type_Id(professorId, TypeId):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    page = request.args.get('page', 1, type=int)  
    limit = request.args.get('limit', 10, type=int)  

    query = Course.query.filter_by(courses_professor_id=professorId)

    if TypeId == 5:
        query = query.filter_by(courses_active=True)
    elif TypeId == 6:
        query = query.filter_by(courses_active=False)
    elif TypeId != 3:
        return jsonify({'message': 'Invalid TypeId'}), 400

    paginated_courses = query.paginate(page=page, per_page=limit, error_out=False)

    result = courses_schema.dump(paginated_courses.items)
    
    if not result:
         return jsonify({'message': 'Courses not found'}), 404

    result = courses_basic_schema.dump(paginated_courses.items)

    return jsonify({
        'courses': result,  
        'total': paginated_courses.total, 
        'page': page,  
        'pages': paginated_courses.pages  
    })

@bp.route("/courses/student/<int:studentId>/type/<int:TypeId>", methods=["GET"])
def get_courses_student_by_type_Id(studentId, TypeId):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    try:
         user_id = get_user_id_from_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
  
    page = request.args.get('page', 1, type=int)  
    limit = request.args.get('limit', 10, type=int)  

    if TypeId == 1:
        courses = db.session.query(Course).\
            join(Enrollment, Enrollment.enrollments_course_id == Course.courses_id).\
            filter(Enrollment.enrollments_student_id == studentId, Enrollment.enrollments_finalized == False)
    elif TypeId == 2:
        courses = db.session.query(Course).\
            join(Enrollment, Enrollment.enrollments_course_id == Course.courses_id).\
            filter(Enrollment.enrollments_student_id == studentId, Enrollment.enrollments_finalized == True)  
    elif TypeId == 4:  
        courses = db.session.query(Course).\
            join(Favorite, Favorite.favorites_course_id == Course.courses_id).\
            filter(Favorite.favorites_user_id == user_id)
    else: 
        return jsonify({'message': 'Invalid TypeId'}), 400

    paginated_courses = courses.paginate(page=page, per_page=limit, error_out=False)

    result = courses_schema.dump(paginated_courses.items)
    
    if not result:
         return jsonify({'message': 'Courses not found'}), 404

    result = courses_basic_schema.dump(paginated_courses.items)

    return jsonify({
        'courses': result,  
        'total': paginated_courses.total, 
        'page': page,  
        'pages': paginated_courses.pages  
    })

@bp.route("/courses/student_id/<studentId>", methods=["GET"])
def get_courses_by_student_id(studentId):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    enrollments = Enrollment.query.filter_by(enrollments_student_id=studentId).all()

    if not enrollments:
        return jsonify({'message': 'No enrollments found for this student'}), 404
        
    course_ids = [enrollment.enrollments_course_id for enrollment in enrollments]

    courses = Course.query.filter(Course.courses_id.in_(course_ids)).all()

    if courses is None:
        return jsonify({'message': 'Courses not found'}), 404
    
    return courses_basic_schema.jsonify(courses), 200

@bp.route("/courses/favorites/<userId>", methods=["GET"])
def get_courses_by_favorites(userId):

    auth_header = request.headers.get('Authorization')
    
    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    favorite_courses = Favorite.query.filter_by(favorites_user_id=userId).all()

    if not favorite_courses:
        return jsonify({'message': 'No favorite courses found for this user'}), 404

    favorite_course_ids = [fav.favorites_course_id for fav in favorite_courses]

    courses = Course.query.filter(Course.courses_id.in_(favorite_course_ids)).all()

    if not courses:
        return jsonify({'message': 'No courses found for this user'}), 404
  
    return courses_basic_schema.jsonify(courses), 200


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
    course.courses_active = data.get('courses_active', course.courses_active)

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
    
    data = request.form 
    courses_image_file = request.files.get('file')

    if 'courses_title' in data and data['courses_title'].strip():
        course.courses_title = data['courses_title']
    if 'courses_content' in data and data['courses_content'].strip():
        course.courses_content = data['courses_content']
    if 'courses_price' in data and data['courses_price'].strip():
        course.courses_price = data['courses_price']
    if 'courses_discounted_price' in data and data['courses_discounted_price'].strip():
        course.courses_discounted_price = data['courses_discounted_price']
    if 'courses_professor_id' in data and data['courses_professor_id'].strip():
        course.courses_professor_id = data['courses_professor_id']
    if 'courses_studycenter_id' in data and data['courses_studycenter_id'].strip():
        course.courses_studycenter_id = data['courses_studycenter_id']
    if 'courses_category_id' in data and data['courses_category_id'].strip():
        course.courses_category_id = data['courses_category_id']
    if 'courses_active' in data and data['courses_active'].strip():
        course.courses_active = data['courses_active'].lower() == 'true'

    if courses_image_file:
        if course.courses_image:
            other_courses_with_same_image = Course.query.filter(Course.courses_image == course.courses_image, Course.courses_id != id).count()

            if other_courses_with_same_image == 0:  
                try:
                    image_filename = os.path.basename(course.courses_image)
                    image_path = os.path.join('app', 'static', 'uploads', image_filename)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    else:
                        print("El archivo no existe en la ruta especificada.")  
                except Exception as e:
                    return jsonify({'error': 'Failed to delete the image file', 'details': str(e)}), 500

        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename, error = save_file(courses_image_file, upload_folder)

        if error:
            return jsonify({'error': error}), 400

        if filename:  
            file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
            course.courses_image = file_url  
        else:
            course.courses_image = None

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

    other_courses_with_same_image = Course.query.filter(
        Course.courses_image == course.courses_image, 
        Course.courses_id != id
    ).count()

    db.session.delete(course)
    db.session.commit()

    if image_path and os.path.exists(image_path) and other_courses_with_same_image == 0:
        try:
            os.remove(image_path)
        except Exception as e:
            return jsonify({'error': 'Failed to delete the image file', 'details': str(e)}), 500

    response = jsonify({'message': 'Course deleted'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# Un endpoint especifico para eliminar la imagen
@bp.route("/course/<id>/delete-image", methods=["DELETE"])
def delete_course_image(id):
    auth_header = request.headers.get('Authorization')

    try:
        decoded_token = decode_token(auth_header)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    course = Course.query.get(id)

    if course is None:
        return jsonify({'message': 'Course not found'}), 404

    if course.courses_image:
        try:
            delete_course_image(course.courses_image)
            
            course.courses_image = None
            db.session.commit()

            return jsonify({'message': 'Image deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to delete the image file', 'details': str(e)}), 500
    else:
        return jsonify({'message': 'No image to delete'}), 400



