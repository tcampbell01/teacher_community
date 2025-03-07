from flask import Blueprint, jsonify, request
from ..models import Group, db, Course

bp = Blueprint('groups', __name__, url_prefix='/groups')

# Utility function to handle error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

@bp.route('', methods=['GET'])
def index():
    """Get a list of all groups."""
    groups = Group.query.all()
    result = [group.serialize() for group in groups]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific group by ID."""
    group = Group.query.get_or_404(id)
    return jsonify(group.serialize())

@bp.route('', methods=['POST'])
def create():
    """Create a new group."""
    if not request.json or not all(field in request.json for field in ['group_name', 'course_id']):
        return error_response("Missing required fields: group_name, course_id.", 400)
    
    group_data = request.json
    
    # Check if the course_id exists
    course = Course.query.get(group_data['course_id'])
    if not course:
        return error_response("Course ID does not exist.", 400)
    
    group = Group(
        group_name=group_data['group_name'],
        group_description=group_data.get('group_description'),
        course_id=group_data['course_id']
    )

    try:
        db.session.add(group)
        db.session.commit()
        return jsonify(group.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating group: {str(e)}", 500)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing group's details."""
    group = Group.query.get_or_404(id)
    
    if not request.json:
        return error_response("No data provided to update.", 400)
    
    group_data = request.json
    
    if 'group_name' in group_data:
        group.group_name = group_data['group_name']
    if 'group_description' in group_data:
        group.group_description = group_data['group_description']
    if 'course_id' in group_data:
        course = Course.query.get(group_data['course_id'])
        if not course:
            return error_response("Course ID does not exist.", 400)
        group.course_id = group_data['course_id']
    
    try:
        db.session.commit()
        return jsonify(group.serialize())
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating group: {str(e)}", 500)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Delete a group by ID."""
    group = Group.query.get_or_404(id)
    
    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify({"message": "Group deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting group: {str(e)}", 500)
