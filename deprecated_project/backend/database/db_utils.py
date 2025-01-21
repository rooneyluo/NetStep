from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import logging
import os
from dotenv import load_dotenv
from model.user_model import UserResponse, UserLogin

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Get database URL from environment variables
DATABASE_URL = str(os.getenv("DATABASE_URL"))

# Configure SQLAlchemy connection pool
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_query(db, query, params=None):
    try:
        if params:
            result = db.execute(query, params).fetchone()
        else:
            result = db.execute(query).fetchone()
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        logger.error(f"Error executing query: {e}", exc_info=True)
        return None

# Function to insert a new user
def add_user(username, password, email, role='user', photo=None):
    insert_query = text("""
    INSERT INTO users (username, password, email, role, photo)
    VALUES (:username, :password, :email, :role, :photo)
    RETURNING username, email, role;
    """)

    params = {
        "username": username,
        "password": password,
        "email": email,
        "role": role,
        "photo": photo
    }
    
    with SessionLocal() as db:
        new_user = execute_query(db, insert_query, params)

    if new_user:
        logger.info(f"User {username} added successfully!")
        return UserResponse(username=new_user.username, email=new_user.email, role=new_user.role)
    else:
        logger.error(f"Failed to add user {username}")
        return None

# Function to fetch a user by username, email or phone number
def get_user_for_authentication(username=None, email=None, phone_number=None):
    select_query = text("""
    SELECT * FROM users WHERE username = :username OR email = :email OR phone_number = :phone_number;
    """)

    params = {
        "username": username,
        "email": email,
        "phone_number": phone_number
    }

    with SessionLocal() as db:
        user = execute_query(db, select_query, params)

    if user:
        logger.info(f"User {username or email or phone_number} fetched successfully!")
        return UserLogin(username=user.username, email=user.email, role=user.role, password=user.password)
    else:
        logger.error(f"Failed to fetch user {username}")
        return None
    
# Function to fetch all users
def fetch_all_users():
    select_query = "SELECT * FROM users;"
    
    with SessionLocal() as db:
        try:
            users = db.execute(select_query).fetchall()
            if users:
                logger.info("Fetched all users successfully!")
                return [UserResponse(
                    username=user.username,
                    email=user.email,
                    role=user.role
                ) for user in users]
            else:
                return []
        except Exception as e:
            logger.error(f"Error fetching users: {e}", exc_info=True)
            return []

# Function to add an event
def add_event(title, description, organizer_id, location_id, start_time, end_time, created_by, updated_by, current_participants, max_participants, status, tags, likes, dislikes):
    insert_query = """
    INSERT INTO events (title, description, organizer_id, location_id, start_time, end_time, created_by, updated_by, current_participants, max_participants, status, tags, likes, dislikes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING title, description, organizer_id, location_id, start_time, end_time, created_by, current_participants, max_participants, status, tags, likes, dislikes;
    """
    params = (title, description, organizer_id, location_id, start_time, end_time, created_by, updated_by, current_participants, max_participants, status, tags, likes, dislikes)
    
    with SessionLocal() as db:
        new_event = execute_query(db, insert_query, params)

    if new_event:
        logger.info(f"Event {title} added successfully!")
        return new_event
    else:
        logger.error(f"Failed to add event {title}")
        return None

# Function to fetch all events
def fetch_all_events():
    select_query = "SELECT title, description, organizer_id, location_id, start_time, end_time, created_by, current_participants, max_participants, status, tags, likes, dislikes FROM events"
    
    with SessionLocal() as db:
        try:
            events = db.execute(select_query).fetchall()
            logger.info("Fetched all events successfully!")
            return events
        except Exception as e:
            logger.error(f"Error fetching events: {e}", exc_info=True)
            return []
        
# Function to fetch a user profile
def get_user_profile(email):
    select_query = text("""
    SELECT username, email, role FROM users WHERE email = :email;
    """)

    params = {
        "email": email
    }

    with SessionLocal() as db:
        user = execute_query(db, select_query, params)

    if user:
        logger.info(f"User {email} fetched successfully!")
        return UserResponse(
            username=user.username,
            email=user.email,
            role=user.role
        )
    else:
        logger.error(f"Failed to fetch user {email}")
        return None
    
# Function to update user information
def update_user_info(current_user, user_update):
    update_query = text("""
    UPDATE users
    SET username = :username, first_name = :first_name, last_name = :last_name, phone_number = :phone_number, photo = :photo
    WHERE email = :email
    RETURNING username, email, role, first_name, last_name, phone_number, photo;
    """)

    params = {
        "email": current_user.email,
        "username": user_update.username,
        "first_name": user_update.first_name,
        "last_name": user_update.last_name,
        "phone_number": user_update.phone_number,
        "photo": user_update.photo
    }

    with SessionLocal() as db:
        updated_user = execute_query(db, update_query, params)

    if updated_user:
        logger.info(f"User {updated_user.email} updated successfully!")
        return UserResponse(username=updated_user.username, email=current_user.email, role=updated_user.role, first_name=updated_user.first_name, last_name=updated_user.last_name, phone_number=updated_user.phone_number, photo=updated_user.photo)
    else:
        logger.error(f"Failed to update user {updated_user.email}")
        return None