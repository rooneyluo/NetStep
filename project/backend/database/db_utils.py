from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.user_model import UserResponse
import logging
import os
from dotenv import load_dotenv

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
def add_user(username, password, email, first_name=None, last_name=None, role='user', photo=None):
    insert_query = """
    INSERT INTO users (username, password, email, first_name, last_name, role, photo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING username, password, email;
    """
    params = (username, password, email, first_name, last_name, role, photo)
    
    with SessionLocal() as db:
        new_user = execute_query(db, insert_query, params)

    if new_user:
        logger.info(f"User {username} added successfully!")
        return UserResponse(username=new_user[0], email=new_user[2])
    else:
        logger.error(f"Failed to add user {username}")
        return None

# Function to fetch a user by username or email
def get_user_by_username_or_email(identifier):
    select_query = "SELECT * FROM users WHERE username = %s OR email = %s;"
    params = (identifier, identifier)
    
    with SessionLocal() as db:
        user = execute_query(db, select_query, params)

    if user:
        logger.info(f"User {identifier} fetched successfully!")
        return UserResponse(username=user[1], email=user[3])  # Assuming user[1] is username, user[3] is email
    else:
        logger.error(f"Failed to fetch user {identifier}")
        return None

# Function to fetch all users
def fetch_all_users():
    select_query = "SELECT * FROM users;"
    
    with SessionLocal() as db:
        try:
            users = db.execute(select_query).fetchall()
            if users:
                logger.info("Fetched all users successfully!")
                return [UserResponse(username=user[1], email=user[3]) for user in users]
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

# Function to get all events
def get_all_events():
    select_query = "SELECT title, description, organizer_id, location_id, start_time, end_time, created_by, current_participants, max_participants, status, tags, likes, dislikes FROM events"
    
    with SessionLocal() as db:
        try:
            events = db.execute(select_query).fetchall()
            logger.info("Fetched all events successfully!")
            return events
        except Exception as e:
            logger.error(f"Error fetching events: {e}", exc_info=True)
            return []