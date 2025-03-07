from flask import Blueprint, jsonify, request
from ..models import Feedback, db, Event, Course

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

# Utility function to handle error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

@bp.route('', methods=['GET'])
def index():
    """Get a list of all feedbacks."""
    feedbacks = Feedback.query.all()
    result = [feedback.serialize() for feedback in feedbacks]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific feedback by ID."""
    feedback = Feedback.query.get_or_404(id)
    return jsonify(feedback.serialize())

@bp.route('', methods=['POST'])
def create():
    """Create a new feedback."""
    if not request.json or 'rating' not in request.json:
        return error_response("Missing required fields: rating.", 400)
    
    feedback_data = request.json
    rating = feedback_data['rating']
    
    # Validate rating range (for example, between 1 and 5)
    if rating < 1 or rating > 5:
        return error_response("Rating must be between 1 and 5.", 400)
    
    # Optional: Check if event_id or course_id exists if provided
    if 'event_id' in feedback_data:
        event = Event.query.get(feedback_data['event_id'])
        if not event:
            return error_response("Event ID does not exist.", 400)
    
    if 'course_id' in feedback_data:
        course = Course.query.get(feedback_data['course_id'])
        if not course:
            return error_response("Course ID does not exist.", 400)
    
    # Create the Feedback instance
    feedback = Feedback(
        rating=rating,
        comments=feedback_data.get('comments'),
        event_id=feedback_data.get('event_id'),
        course_id=feedback_data.get('course_id')
    )

    try:
        db.session.add(feedback)
        db.session.commit()
        return jsonify(feedback.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating feedback: {str(e)}", 500)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing feedback."""
    feedback = Feedback.query.get_or_404(id)
    
    if not request.json:
        return error_response("No data provided to update.", 400)
    
    feedback_data = request.json

    if 'rating' in feedback_data:
        rating = feedback_data['rating']
        if rating < 1 or rating > 5:
            return error_response("Rating must be between 1 and 5.", 400)
        feedback.rating = rating
    
    if 'comments' in feedback_data:
        feedback.comments = feedback_data['comments']
    
    if 'event_id' in feedback_data:
        event = Event.query.get(feedback_data['event_id'])
        if not event:
            return error_response("Event ID does not exist.", 400)
        feedback.event_id = feedback_data['event_id']
    
    if 'course_id' in feedback_data:
        course = Course.query.get(feedback_data['course_id'])
        if not course:
            return error_response("Course ID does not exist.", 400)
        feedback.course_id = feedback_data['course_id']
    
    try:
        db.session.commit()
        return jsonify(feedback.serialize())
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating feedback: {str(e)}", 500)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Delete feedback by ID."""
    feedback = Feedback.query.get_or_404(id)
    
    try:
        db.session.delete(feedback)
        db.session.commit()
        return jsonify({"message": "Feedback deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting feedback: {str(e)}", 500)
