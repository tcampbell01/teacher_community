from flask import Blueprint, jsonify, request
from ..models import User, CourseCreators, db

bp = Blueprint('user_course_creator', __name__, url_prefix='/user_course_creator')

# Utility function to handle error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

@bp.route('/<int:user_id>', methods=['GET'])
def get_user_creators(user_id: int):
    """Get all course creators associated with a user."""
    user = User.query.get_or_404(user_id)
    creators = user.course_creators
    result = [creator.serialize() for creator in creators]
    return jsonify(result)

@bp.route('/<int:user_id>/add/<int:creator_id>', methods=['POST'])
def add_course_creator(user_id: int, creator_id: int):
    """Associate a user with a course creator."""
    user = User.query.get_or_404(user_id)
    creator = CourseCreators.query.get_or_404(creator_id)
    
    # Check if creator is already associated
    if creator in user.course_creators:
        return error_response("This creator is already associated with the user.", 400)
    
    user.course_creators.append(creator)
    
    try:
        db.session.commit()
        return jsonify({"message": "Course creator added successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error adding course creator: {str(e)}", 500)

@bp.route('/<int:user_id>/remove/<int:creator_id>', methods=['DELETE'])
def remove_course_creator(user_id: int, creator_id: int):
    """Remove a course creator association for a user."""
    user = User.query.get_or_404(user_id)
    creator = CourseCreators.query.get_or_404(creator_id)
    
    # Check if creator is not associated
    if creator not in user.course_creators:
        return error_response("This creator is not associated with the user.", 400)
    
    user.course_creators.remove(creator)
    
    try:
        db.session.commit()
        return jsonify({"message": "Course creator removed successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error removing course creator: {str(e)}", 500)
