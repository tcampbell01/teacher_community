from flask import Blueprint, jsonify, request, abort
from ..models import Course, db, CourseCreators

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('', methods=['GET'])
def index():
    """Get a list of all courses."""
    courses = Course.query.all()
    result = [course.serialize() for course in courses]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific course by ID."""
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize())

@bp.route('', methods=['POST'])
def create():
    """Create a new course."""
    if not request.json or not all(field in request.json for field in ['course_name', 'course_description', 'creator_id']):
        return abort(400, description="Missing required fields: course_name, course_description, or creator_id.")
    
    course_data = request.json
    creator = CourseCreators.query.get(course_data['creator_id'])
    
    if not creator:
        return abort(400, description="Creator ID does not exist.")
    
    course = Course(
        course_name=course_data['course_name'],
        course_description=course_data['course_description'],
        creator_id=course_data['creator_id']
    )

    try:
        db.session.add(course)
        db.session.commit()
        return jsonify(course.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing course's details."""
    course = Course.query.get_or_404(id)
    
    if not request.json:
        return abort(400, description="No data provided to update.")
    
    course_data = request.json

    if 'course_name' in course_data:
        course.course_name = course_data['course_name']
    if 'course_description' in course_data:
        course.course_description = course_data['course_description']
    if 'creator_id' in course_data:
        creator = CourseCreators.query.get(course_data['creator_id'])
        if not creator:
            return abort(400, description="Creator ID does not exist.")
        course.creator_id = course_data['creator_id']
    
    try:
        db.session.commit()
        return jsonify(course.serialize())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Delete a course by ID."""
    course = Course.query.get_or_404(id)
    
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
