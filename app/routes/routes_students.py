from flask import Blueprint, request, jsonify
from app.models import Student
from app.schema.student_schema import StudentSchema
from app import db

# Definir el blueprint para las rutas de User
bp = Blueprint('students', __name__)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@bp.route('/student', methods=["POST"])
def add_student():
    
    data = request.json

    required_fields = ['students_first_name', 'students_last_name', 'students_user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es obligatorio'}), 400

    students_first_name = data['students_first_name']
    students_last_name = data['students_last_name']
    students_user_id = data['students_user_id']

    existing_student = Student.query.filter_by(students_user_id=students_user_id).first()
    if existing_student:
        return jsonify({'error': 'El estudiante ya existe'}), 400

    new_student = Student(students_first_name=students_first_name, students_last_name=students_last_name, students_user_id=students_user_id)
    
    try:
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el estudiante', 'details': str(e)}), 500

    student = Student.query.get(new_student.students_id)
    return student_schema.jsonify(student), 201

    
@bp.route('/students', methods=["GET"])
def all_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    
    return jsonify(result)

@bp.route("/student/<id>", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    return student_schema.jsonify(student)

@bp.route("/student/<id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    data = request.json
    student.students_first_name = data.get('students_first_name', student.students_first_name)
    student.students_last_name = data.get('students_last_name', student.students_last_name)
    student.students_user_id = data.get('students_user_id', student.students_user_id)

    db.session.commit()

    return student_schema.jsonify(student)

@bp.route("/student/<id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': 'Student deleted'})