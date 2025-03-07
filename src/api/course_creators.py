from flask import Blueprint, jsonify, request, abort
from ..models import CourseCreators, db

bp = Blueprint('course_creators', __name__, url_prefix='/course_creators')

@bp.route('', methods=['GET'])
def index():
    """Get a list of all course creators."""
    creators = CourseCreators.query.all()
    result = [creator.serialize() for creator in creators]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    """Get a specific course creator by ID."""
    creator = CourseCreators.query.get_or_404(id)
    return jsonify(creator.serialize())

@bp.route('', methods=['POST'])
def create():
    """Create a new course creator."""
    if not request.json or not all(field in request.json for field in [
        'creator_name', 'creator_email', 'creator_phone_number', 'creator_address', 
        'creator_city', 'creator_state', 'creator_zip_code', 'creator_country']):
        return abort(400, description="Missing required fields in the request.")
    
    creator_data = request.json
    creator = CourseCreators(
        creator_name=creator_data['creator_name'],
        creator_email=creator_data['creator_email'],
        creator_phone_number=creator_data['creator_phone_number'],
        creator_address=creator_data['creator_address'],
        creator_city=creator_data['creator_city'],
        creator_state=creator_data['creator_state'],
        creator_zip_code=creator_data['creator_zip_code'],
        creator_country=creator_data['creator_country']
    )

    try:
        db.session.add(creator)
        db.session.commit()
        return jsonify(creator.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    """Update an existing course creator's details."""
    creator = CourseCreators.query.get_or_404(id)
    
    if not request.json:
        return abort(400, description="No data provided to update.")
    
    creator_data = request.json

    if 'creator_name' in creator_data:
        creator.creator_name = creator_data['creator_name']
    if 'creator_email' in creator_data:
        creator.creator_email = creator_data['creator_email']
    if 'creator_phone_number' in creator_data:
        creator.creator_phone_number = creator_data['creator_phone_number']
    if 'creator_address' in creator_data:
        creator.creator_address = creator_data['creator_address']
    if 'creator_city' in creator_data:
        creator.creator_city = creator_data['creator_city']
    if 'creator_state' in creator_data:
        creator.creator_state = creator_data['creator_state']
    if 'creator_zip_code' in creator_data:
        creator.creator_zip_code = creator_data['creator_zip_code']
    if 'creator_country' in creator_data:
        creator.creator_country = creator_data['creator_country']

    try:
        db.session.commit()
        return jsonify(creator.serialize())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Delete a course creator by ID."""
    creator = CourseCreators.query.get_or_404(id)
    
    try:
        db.session.delete(creator)
        db.session.commit()
        return jsonify({"message": "Course creator deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
