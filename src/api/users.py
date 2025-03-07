from flask import Blueprint, jsonify, request, abort
from ..models import User, db
import hashlib
import secrets
import datetime

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

# Utility function to handle error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

bp = Blueprint('users', __name__, url_prefix='/users')

# List all users
@bp.route('', methods=['GET'])
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = [u.serialize() for u in users]  # serialize each user
    return jsonify(result)  # return JSON response

# Get a specific user
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())

# Create a new user
@bp.route('', methods=['POST'])
def create():
    if 'email' not in request.json or 'password' not in request.json:
        return error_response("Missing email or password", 400)
    
    email = request.json['email']
    password = request.json['password']
    
    if len(password) < 8:
        return error_response("Password must be at least 8 characters", 400)
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return error_response("User with that email already exists.", 400)
    
    # Create the user
    u = User(
        email=email,
        password=scramble(password),
        first_name=request.json.get('first_name', ''),
        last_name=request.json.get('last_name', ''),
        phone_number=request.json.get('phone_number', ''),
        address=request.json.get('address', ''),
        city=request.json.get('city', ''),
        state=request.json.get('state', ''),
        zip_code=request.json.get('zip_code', ''),
        country=request.json.get('country', ''),
        consent_for_marketing=request.json.get('consent_for_marketing', False),
        created_on=datetime.datetime.utcnow(),
        role=request.json.get('role', 'student')  # default role 'student'
    )
    
    try:
        db.session.add(u)
        db.session.commit()
        return jsonify(u.serialize()), 201  # Return 201 Created status
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating user: {str(e)}", 500)

# Delete a user
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return error_response(f"Error deleting user: {str(e)}", 500)

# Update user data
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
    
    if 'email' not in request.json and 'password' not in request.json:
        return error_response("No data provided to update", 400)
    
    if 'email' in request.json:
        email = request.json['email']
        u.email = email
    
    if 'password' in request.json:
        password = request.json['password']
        if len(password) < 8:
            return error_response("Password must be at least 8 characters", 400)
        u.password = scramble(password)  # Scramble the password
    
    try:
        db.session.commit()
        return jsonify(u.serialize()), 200  # Return the updated user record
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return error_response(f"Error updating user: {str(e)}", 500)

# Get courses that the user is enrolled in
@bp.route('/<int:id>/enrolled_courses', methods=['GET'])
def enrolled_courses(id: int):
    u = User.query.get_or_404(id)
    result = [enrollment.course.serialize() for enrollment in u.enrollments]  # Serialize each course
    return jsonify(result)

# Get feedback provided by the user for courses
@bp.route('/<int:id>/feedbacks', methods=['GET'])
def user_feedbacks(id: int):
    u = User.query.get_or_404(id)
    result = [feedback.serialize() for feedback in u.feedbacks]  # Serialize each feedback
    return jsonify(result)

# Get all courses created by the user (based on user-course creator relationships)
@bp.route('/<int:id>/created_courses', methods=['GET'])
def created_courses(id: int):
    u = User.query.get_or_404(id)
    result = [course_creator.serialize() for course_creator in u.created_courses]  # Serialize each course
    return jsonify(result)
