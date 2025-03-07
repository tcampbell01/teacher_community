from flask import Blueprint, jsonify, request, abort
from ..models import ConsentForMarketing, User, db

bp = Blueprint('consent', __name__, url_prefix='/consent')

@bp.route('', methods=['POST'])
def create_consent():
    """Create a new consent record for a user."""
    if 'user_id' not in request.json or 'consent' not in request.json:
        return abort(400, description="Missing user_id or consent status in the request.")
    
    user_id = request.json['user_id']
    consent_status = request.json['consent']
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User not found.")
    
    # Check if consent record already exists for the user
    existing_consent = ConsentForMarketing.query.filter_by(user_id=user_id).first()
    if existing_consent:
        return abort(400, description="Consent record already exists for this user.")
    
    consent = ConsentForMarketing(
        user_id=user_id,
        consent=consent_status
    )
    
    try:
        db.session.add(consent)
        db.session.commit()
        return jsonify({"message": "Consent recorded successfully", "consent": consent.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('<int:id>', methods=['GET'])
def get_consent(id: int):
    """Get the consent status for a specific user."""
    consent = ConsentForMarketing.query.get_or_404(id)
    return jsonify(consent.serialize())

@bp.route('<int:id>', methods=['PUT', 'PATCH'])
def update_consent(id: int):
    """Update the consent status for a specific user."""
    consent = ConsentForMarketing.query.get_or_404(id)
    
    if 'consent' not in request.json:
        return abort(400, description="Consent status is required to update.")
    
    consent_status = request.json['consent']
    
    consent.consent = consent_status
    consent.changed_on = db.func.current_timestamp()  # Update the timestamp of the change
    
    try:
        db.session.commit()
        return jsonify({"message": "Consent updated successfully", "consent": consent.serialize()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('<int:id>', methods=['DELETE'])
def delete_consent(id: int):
    """Delete a consent record for a specific user."""
    consent = ConsentForMarketing.query.get_or_404(id)
    
    try:
        db.session.delete(consent)
        db.session.commit()
        return jsonify({"message": "Consent record deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
