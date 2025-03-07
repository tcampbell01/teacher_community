from flask import Blueprint, jsonify, request, abort
from ..models import Event, db
import datetime

bp = Blueprint('events', __name__, url_prefix='/events')

# Utility function to handle error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

# Utility function to validate the event date format
def validate_event_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None

@bp.route('', methods=['GET'])
def index():
    """Get a list of all events."""
    events = Event.query.all()
    result = [event.serialize() for event in events]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific event by ID."""
    event = Event.query.get_or_404(id)
    return jsonify(event.serialize())

@bp.route('', methods=['POST'])
def create():
    """Create a new event."""
    if not request.json or not all(field in request.json for field in ['event_name', 'event_description', 'event_date', 'location']):
        return error_response("Missing required fields: event_name, event_description, event_date, or location.", 400)
    
    event_data = request.json

    # Validate event date
    event_date = validate_event_date(event_data['event_date'])
    if not event_date:
        return error_response("Invalid event_date format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS).", 400)
    
    try:
        event = Event(
            event_name=event_data['event_name'],
            event_description=event_data['event_description'],
            event_date=event_date,  # Using the validated event date
            location=event_data['location']
        )
        
        db.session.add(event)
        db.session.commit()
        return jsonify(event.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating event: {str(e)}", 500)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing event's details."""
    event = Event.query.get_or_404(id)
    
    if not request.json:
        return error_response("No data provided to update.", 400)
    
    event_data = request.json

    if 'event_name' in event_data:
        event.event_name = event_data['event_name']
    if 'event_description' in event_data:
        event.event_description = event_data['event_description']
    if 'event_date' in event_data:
        event_date = validate_event_date(event_data['event_date'])
        if not event_date:
            return error_response("Invalid event_date format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS).", 400)
        event.event_date = event_date  # Update the event_date with the validated date
    if 'location' in event_data:
        event.location = event_data['location']
    
    try:
        db.session.commit()
        return jsonify(event.serialize())
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating event: {str(e)}", 500)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Delete an event by ID."""
    event = Event.query.get_or_404(id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting event: {str(e)}", 500)
