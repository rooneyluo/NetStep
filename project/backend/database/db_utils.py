from model.user_model import UserResponse
from database.database_connection_manager import DatabaseConnectionManager
from .db_config import db_config  # Configuration for database connection

# Function to insert a new user
def add_user(username, password, email, first_name=None, last_name=None, role='user', photo=None):
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO users (username, password, email, first_name, last_name, role, photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING username, password, email;
                """

                cur.execute(insert_query, (username, password, email, first_name, last_name, role, photo))
                new_user = cur.fetchone()

                conn.commit()
                
                print("User added successfully!")

                return UserResponse(username=new_user[0], email=new_user[2])
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error adding user: {e}")
        return None

# Function to fetch a user by username
def get_user_by_username(email):
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM users WHERE username = %s OR email = %s;"

                cur.execute(query, (email, email))

                user = cur.fetchone()

                if user is None:
                    return None
                
                return UserResponse(username=user[1], email=user[3])
            
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None


# Function to fetch all users
def fetch_all_users():
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM users;"

                cur.execute(query)
                users = cur.fetchall()

                if users is None:
                    return []
                
                return [UserResponse(username=user[1], email=user[3]) for user in users]
   
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    
def add_event(name, location, start_time, end_time, description, create_by):
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                # get user id
                query = "SELECT * FROM users WHERE username = %s OR email = %s;"
                cur.execute(query, (create_by, create_by))

                user = cur.fetchone()

                if user is None:
                    return None
                
                user_id = user[0]

                # insert event
                insert_query = """
                INSERT INTO events (name, location, start_time, end_time, description, create_by)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, location, start_time, end_time, description, create_by;
                """

                cur.execute(insert_query, (name, location, start_time, end_time, description, user_id))
                new_event = cur.fetchone()

                conn.commit()
                
                print("Event added successfully!")
                
                return new_event
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error adding event: {e}")

        return None
    
def get_all_events():
    conn = None
    cur = None
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                query = "SELECT name, location, start_time, end_time, description FROM events;"
                cur.execute(query)
                events = cur.fetchall()

                if events is None:
                    return []
                
                return events
    
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []