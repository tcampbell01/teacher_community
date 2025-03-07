import os

class Config:
    # Database URI configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@pg:5432/teacher_community'

    # Disable Flask SQLAlchemy modification tracking (recommended for performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Disable CSRF protection (only for testing, not recommended for production)
    WTF_CSRF_ENABLED = False
