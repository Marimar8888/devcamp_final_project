from flask import Blueprint, request, jsonify
from app.models import StudyCenter, Student, StudyCenterStudent
from app.schema.studycenter_student_schema import StudyCenterStudentSchema

from app import db

bp = Blueprint('studycenter_student', __name__)

studycenter_student_schema = StudyCenterStudentSchema()
studycenter_students_schema = StudyCenterStudentSchema(many=True)

@bp.route('/studycenter_student', methods=["POST"])
def add_studyCenter_student():
    data = request.json

    required_fields = ['studycenter_student_student_id', 'studycenter_student_center_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    studyCenter_id = data['studycenter_student_center_id']
    student_id = data['studycenter_student_student_id']

    studyCenter = StudyCenter.query.get(studyCenter_id)
    student = Student.query.get(student_id)

    if not studyCenter:
        return jsonify({'error': 'StudyCenter not found'}), 404
    
    if not student:
        return jsonify({'error': 'Student not found'}), 400

    existing_relationship = StudyCenterStudent.query.filter_by(
        studycenter_student_center_id=studyCenter_id, 
        studycenter_student_student_id=student_id
    ).first()

    if existing_relationship:
        return jsonify({'error': 'The student already exists in that center'}), 400
    
    new_relationship = StudyCenterStudent(
        studycenter_student_student_id=student_id, 
        studycenter_student_center_id=studyCenter_id
    )

    try:
        db.session.add(new_relationship)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Relationship could not be added'})

    return jsonify({'message': 'Successfully Added Relationship'}), 201

@bp.route('/studycenter_students', methods=["GET"])
def all_studycenter_students():
    all_studycenter_students = StudyCenterStudent.query.all()
    result = studycenter_students_schema.dump(all_studycenter_students)
    return jsonify(result)