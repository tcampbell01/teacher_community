from flask import Flask
from flask_migrate import Migrate
from src.models import db  # Assuming your db is initialized in src/models.py
from src.api import consent, course_creators, courses, enrollments, events, feedback, groups, user_course_creator, users

# Create the Flask app
app = Flask(__name__)

# Configure the app (ensure that the database URI is set correctly)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nucamp@pg:5432/teacher_community'  # Change this if necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable Flask-SQLAlchemy's modification tracking

# Print the database URI to verify it's being set correctly
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
print(app.config)  # This will print all the configuration settings

# Initialize the database and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Register your blueprints
app.register_blueprint(consent.bp)
app.register_blueprint(course_creators.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(enrollments.bp)
app.register_blueprint(events.bp)
app.register_blueprint(feedback.bp)
app.register_blueprint(groups.bp)
app.register_blueprint(user_course_creator.bp)
app.register_blueprint(users.bp)

if __name__ == "__main__":
    app.run(debug=True)
