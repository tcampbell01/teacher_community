from flask import Blueprint, jsonify, request, abort
from ..models import Enrollment, db, User, Course  # Updated Student to User

bp = Blueprint('enrollments', __name__, url_prefix='/enrollments')

@bp.route('', methods=['GET'])
def index():
    """Get a list of all enrollments."""
    enrollments = Enrollment.query.all()
    result = [enrollment.serialize() for enrollment in enrollments]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific enrollment by ID."""
    enrollment = Enrollment.query.get_or_404(id)
    return jsonify(enrollment.serialize())

@bp.route('', methods=['POST'])
def create():
    """Enroll a student in a course."""
    if not request.json or 'student_id' not in request.json or 'course_id' not in request.json:
        return abort(400, description="Missing required fields: student_id, course_id.")
    
    enrollment_data = request.json
    user = User.query.get(enrollment_data['student_id'])  # Replaced Student with User
    course = Course.query.get(enrollment_data['course_id'])
    
    if not user:
        return abort(400, description="Student ID does not exist.")  # Error message adjusted
    if not course:
        return abort(400, description="Course ID does not exist.")
    
    enrollment = Enrollment(
        student_id=enrollment_data['student_id'],  # Ensure this is referring to User
        course_id=enrollment_data['course_id']
    )

    try:
        db.session.add(enrollment)
        db.session.commit()
        return jsonify(enrollment.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing enrollment (e.g., change course for a student)."""
    enrollment = Enrollment.query.get_or_404(id)
    
    if not request.json:
        return abort(400, description="No data provided to update.")
    
    enrollment_data = request.json

    if 'student_id' in enrollment_data:
        user = User.query.get(enrollment_data['student_id'])  # Replaced Student with User
        if not user:
            return abort(400, description="Student ID does not exist.")  # Error message adjusted
        enrollment.student_id = enrollment_data['student_id']
    
    if 'course_id' in enrollment_data:
        course = Course.query.get(enrollment_data['course_id'])
        if not course:
            return abort(400, description="Course ID does not exist.")
        enrollment.course_id = enrollment_data['course_id']
    
    try:
        db.session.commit()
        return jsonify(enrollment.serialize())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Unenroll a student from a course."""
    enrollment = Enrollment.query.get_or_404(id)
    
    try:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
