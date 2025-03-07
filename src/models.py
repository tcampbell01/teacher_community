import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text, nullable=False)
    course_price = db.Column(db.Numeric(10, 2), nullable=False)
    course_end_date = db.Column(db.Date, nullable=False)
    course_purchase_date = db.Column(db.Date, nullable=False)
    course_creator_id = db.Column(db.Integer, db.ForeignKey('course_creator_id.creator_id'), nullable=False)
    
    course_creator = db.relationship('CourseCreator', backref='courses', lazy=True)

    def serialize(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_description': self.course_description,
            'course_price': str(self.course_price),
            'course_end_date': self.course_end_date.isoformat(),
            'course_purchase_date': self.course_purchase_date.isoformat(),
            'course_creator_id': self.course_creator_id
        }

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    consent_for_marketing = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'created_on': self.created_on.isoformat(),
            'consent_for_marketing': self.consent_for_marketing,
            'role': self.role
        }

class UserCourseCreator(db.Model):
    __tablename__ = 'user_course_creator'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('course_creator_id.creator_id'), primary_key=True)

    user = db.relationship('User', backref='user_course_creators', lazy=True)
    creator = db.relationship('CourseCreator', backref='user_course_creators', lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_date = db.Column(db.Date, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    payment_status = db.Column(db.Boolean, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    completion_status = db.Column(db.Boolean, nullable=False)

    course = db.relationship('Course', backref='enrollments', lazy=True)
    user = db.relationship('User', backref='enrollments', lazy=True)
    
    def serialize(self):
        return {
            'enrollment_id': self.enrollment_id,
            'enrollment_date': self.enrollment_date.isoformat(),
            'course_id': self.course_id,
            'user_id': self.user_id,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat(),
            'completion_status': self.completion_status
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedback_date = db.Column(db.Date, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    course = db.relationship('Course', backref='feedbacks', lazy=True)
    user = db.relationship('User', backref='feedbacks', lazy=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='_user_course_uc'),)

    def serialize(self):
        return {
            'feedback_id': self.feedback_id,
            'feedback_date': self.feedback_date.isoformat(),
            'feedback_text': self.feedback_text,
            'course_id': self.course_id,
            'user_id': self.user_id,
            'rating': self.rating
        }

class ConsentForMarketing(db.Model):
    __tablename__ = 'consent_for_marketing'

    consent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    consent_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    consent = db.Column(db.Boolean, nullable=False)
    changed_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = db.relationship('User', backref='consent_for_marketing', lazy=True)
    
    def serialize(self):
        return {
            'consent_id': self.consent_id,
            'consent_date': self.consent_date.isoformat(),
            'user_id': self.user_id,
            'consent': self.consent,
            'changed_on': self.changed_on.isoformat()
        }

class CourseCreators(db.Model):
    __tablename__ = 'course_creator_id'

    creator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_name = db.Column(db.String(100), nullable=False)
    creator_email = db.Column(db.String(100), nullable=False)
    creator_phone_number = db.Column(db.String(100), nullable=False)
    creator_address = db.Column(db.String(100), nullable=False)
    creator_city = db.Column(db.String(100), nullable=False)
    creator_state = db.Column(db.String(100), nullable=False)
    creator_zip_code = db.Column(db.String(100), nullable=False)
    creator_country = db.Column(db.String(100), nullable=False)
    creator_created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            'creator_id': self.creator_id,
            'creator_name': self.creator_name,
            'creator_email': self.creator_email,
            'creator_phone_number': self.creator_phone_number,
            'creator_address': self.creator_address,
            'creator_city': self.creator_city,
            'creator_state': self.creator_state,
            'creator_zip_code': self.creator_zip_code,
            'creator_country': self.creator_country,
            'creator_created_on': self.creator_created_on.isoformat()
        }

class CoursePrerequisite(db.Model):
    __tablename__ = 'course_prerequisites'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
    prerequisite_course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)

    course = db.relationship('Course', foreign_keys=[course_id], backref='prerequisites', lazy=True)
    prerequisite_course = db.relationship('Course', foreign_keys=[prerequisite_course_id], backref='course_prerequisites', lazy=True)

class UserActivity(db.Model):
    __tablename__ = 'user_activity'

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    activity_type = db.Column(db.String(50))
    activity_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref='user_activities', lazy=True)

    def serialize(self):
        return {
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'activity_date': self.activity_date.isoformat()
        }

class Group(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(100), nullable=False)
    group_description = db.Column(db.Text)

    def serialize(self):
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'group_description': self.group_description
        }

class UserGroup(db.Model):
    __tablename__ = 'user_groups'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)

    user = db.relationship('User', backref='user_groups', lazy=True)
    group = db.relationship('Group', backref='user_groups', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    event_description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)

    course = db.relationship('Course', backref='events', lazy=True)

    def serialize(self):
        return {
            'event_id': self.event_id,
            'course_id': self.course_id,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'event_date': self.event_date.isoformat()
        }

class EventEnrollment(db.Model):
    __tablename__ = 'event_enrollments'

    event_enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    user = db.relationship('User', backref='event_enrollments', lazy=True)
    event = db.relationship('Event', backref='event_enrollments', lazy=True)

