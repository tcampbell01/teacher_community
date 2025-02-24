CREATE TABLE courses
(
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_description TEXT NOT NULL,
    course_price DECIMAL(10, 2) NOT NULL,
    course_end_date DATE NOT NULL,
    course_purchase_date DATE NOT NULL,
    course_creator_id INT NOT NULL,
    FOREIGN KEY (course_creator_id) REFERENCES course_creator_id(creator_id) ON DELETE CASCADE  
);

CREATE INDEX idx_courses_course_creator_id ON courses(course_creator_id);

CREATE TABLE users
(
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    consent_for_marketing BOOLEAN NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'student'
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE user_course_creator
(
    user_id INT NOT NULL,
    creator_id INT NOT NULL,
    PRIMARY KEY (user_id, creator_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (creator_id) REFERENCES course_creator_id(creator_id) ON DELETE CASCADE
);

CREATE TABLE enrollments
(
    enrollment_id SERIAL PRIMARY KEY,
    enrollment_date DATE NOT NULL,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    payment_status BOOLEAN NOT NULL,
    payment_date DATE NOT NULL,
    completion_status BOOLEAN NOT NULL
);

CREATE INDEX idx_enrollments_user_id ON enrollments(user_id);
CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);

CREATE TABLE feedback
(
    feedback_id SERIAL PRIMARY KEY,
    feedback_date DATE NOT NULL,
    feedback_text TEXT NOT NULL,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    rating INT NOT NULL,
    CONSTRAINT unique_feedback UNIQUE (user_id, course_id)
);

CREATE INDEX idx_feedback_course_id ON feedback(course_id);
CREATE INDEX idx_feedback_user_id ON feedback(user_id);

CREATE TABLE consent_for_marketing
(
    consent_id SERIAL PRIMARY KEY,
    consent_date DATE NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    consent BOOLEAN NOT NULL,
    changed_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_creator_id
(
    creator_id SERIAL PRIMARY KEY,
    creator_name VARCHAR(100) NOT NULL,
    creator_email VARCHAR(100) NOT NULL,
    creator_phone_number VARCHAR(100) NOT NULL,
    creator_address VARCHAR(100) NOT NULL,
    creator_city VARCHAR(100) NOT NULL,
    creator_state VARCHAR(100) NOT NULL,
    creator_zip_code VARCHAR(100) NOT NULL,
    creator_country VARCHAR(100) NOT NULL,
    creator_created_on TIMESTAMP NOT NULL
);

CREATE TABLE course_prerequisites
(
    course_id INT,
    prerequisite_course_id INT,
    PRIMARY KEY (course_id, prerequisite_course_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id)
);

CREATE TABLE user_activity
(
    activity_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50),
    activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE groups
(
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    group_description TEXT
);

CREATE TABLE user_groups
(
    user_id INT,
    group_id INT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE events
(
    event_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_description TEXT,
    event_date TIMESTAMP NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE event_enrollments
(
    event_enrollment_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
