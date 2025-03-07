import random
import string
import hashlib
import secrets
from faker import Faker
import psycopg2
from psycopg2.extras import execute_batch

# Constants
USER_COUNT = 50
COURSE_COUNT = 20
ENROLLMENT_COUNT = 100
FEEDBACK_COUNT = 200

# PostgreSQL connection parameters
HOST = 'localhost'  # Use 'localhost' instead of 'pg_container'
PORT = 5432
USER = 'postgres'
PASSWORD = ''  # Leave it empty if no password is set in docker-compose.yml
DB_NAME = 'teacher_community'  # Database name

# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    dbname=DB_NAME
)

cur = conn.cursor()

# Initialize Faker instance
fake = Faker()

def random_passhash():
    """Generate a hashed password"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',
            k=random.randint(8, 15)  # Password length between 8 and 15
        )
    )
    salt = secrets.token_hex(16)
    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def insert_course_creator():
    """Insert random course creators into the database"""
    creators = []
    for _ in range(5):  # Assuming we want 5 course creators
        creators.append((
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.address(),
            fake.city(),
            fake.state(),
            fake.zipcode(),
            fake.country(),
            fake.date_this_decade()
        ))
    
    execute_batch(cur, """
        INSERT INTO course_creator_id (creator_name, creator_email, creator_phone_number, 
            creator_address, creator_city, creator_state, creator_zip_code, 
            creator_country, creator_created_on) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, creators)
    conn.commit()


def insert_courses():
    """Insert random courses into the database"""
    courses = []
    for _ in range(COURSE_COUNT):
        creator_id = random.randint(1, 5)  # Random creator_id between 1 and 5
        courses.append((
            fake.company(),
            fake.text(),
            random.uniform(50.0, 500.0),
            fake.date_this_decade(),
            fake.date_this_decade(),
            creator_id
        ))

    execute_batch(cur, """
        INSERT INTO courses (course_name, course_description, course_price, 
            course_end_date, course_purchase_date, course_creator_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, courses)
    conn.commit()


def insert_users():
    """Insert random users into the database"""
    users = []
    for _ in range(USER_COUNT):
        users.append((
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            random_passhash(),
            fake.phone_number(),
            fake.address(),
            fake.city(),
            fake.state(),
            fake.zipcode(),
            fake.country(),
            fake.date_this_decade(),
            random.choice([True, False]),
            random.choice(['student', 'teacher', 'admin'])
        ))

    execute_batch(cur, """
        INSERT INTO users (first_name, last_name, email, password, phone_number, 
            address, city, state, zip_code, country, created_on, consent_for_marketing, role) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, users)
    conn.commit()


def insert_enrollments():
    """Insert random enrollments into the database"""
    enrollments = []
    for _ in range(ENROLLMENT_COUNT):
        course_id = random.randint(1, COURSE_COUNT)
        user_id = random.randint(1, USER_COUNT)
        enrollments.append((
            fake.date_this_year(),
            course_id,
            user_id,
            random.choice([True, False]),
            fake.date_this_year(),
            random.choice([True, False])
        ))

    execute_batch(cur, """
        INSERT INTO enrollments (enrollment_date, course_id, user_id, 
            payment_status, payment_date, completion_status) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, enrollments)
    conn.commit()


def insert_feedback():
    """Insert random feedback into the database"""
    feedback = []
    for _ in range(FEEDBACK_COUNT):
        course_id = random.randint(1, COURSE_COUNT)
        user_id = random.randint(1, USER_COUNT)
        feedback.append((
            fake.date_this_year(),
            fake.text(),
            course_id,
            user_id,
            random.randint(1, 5)
        ))

    execute_batch(cur, """
        INSERT INTO feedback (feedback_date, feedback_text, course_id, 
            user_id, rating) 
        VALUES (%s, %s, %s, %s, %s)
    """, feedback)
    conn.commit()


def main():
    """Main function to insert fake data"""
    insert_course_creator()
    insert_courses()
    insert_users()
    insert_enrollments()
    insert_feedback()
    print("Data inserted successfully.")


# Run the script
if __name__ == "__main__":
    main()

    # Close the connection
    cur.close()
    conn.close()
