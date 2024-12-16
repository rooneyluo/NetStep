import psycopg2
from database.db_config import db_config  # Configuration for database connection
from model.user_model import User

# Function to connect to the database
def get_connection():
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            dbname=db_config['dbname'],
            port=db_config['port']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# create database
def create_database(database_name):
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return

        cur = conn.cursor()

        cur.execute(f"CREATE DATABASE {database_name};")
        print(f"Database {database_name} created successfully!")
    
    except Exception as e:
        print(f"Error creating database: {e}")
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# create tables
def create_tables():
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return

        cur = conn.cursor()

        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                role VARCHAR(50) DEFAULT 'user',
                photo BYTEA,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        print("User table created successfully!")

        # Create events table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                description VARCHAR(255),
                create_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_user FOREIGN KEY (create_by) REFERENCES users(id) ON DELETE CASCADE
        );

            """
        )
        
        print("Events table created successfully!")

        conn.commit()

    
    except Exception as e:
        print(f"Error creating tables: {e}")
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to insert a new user
def add_user(username, password, email, first_name=None, last_name=None, role='user', photo=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return None

        cur = conn.cursor()

        insert_query = """
        INSERT INTO users (username, password, email, first_name, last_name, role, photo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING username, password, email;
        """

        cur.execute(insert_query, (username, password, email, first_name, last_name, role, photo))
        new_user = cur.fetchone()

        conn.commit()
        
        print("User added successfully!")

        return User(username=new_user[0], password=new_user[1], email=new_user[2])
    
    except Exception as e:
        conn.rollback()
        print(f"Error adding user: {e}")
        return None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to fetch a user by username
def get_user_by_username(email):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return None

        cur = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s OR email = %s;"

        cur.execute(query, (email, email))

        user = cur.fetchone()

        if user is None:
            return None
        
        return User(username=user[1], password=user[2], email=user[3])
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to fetch all users
def fetch_all_users():
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return []

        cur = conn.cursor()

        query = "SELECT * FROM users;"
        cur.execute(query)
        users = cur.fetchall()

        if users is None:
            return []
        
        return [User(username=user[1], password=user[2], email=user[3]) for user in users]
    
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_event(name, location, start_time, end_time, description, create_by):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return None

        cur = conn.cursor()

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
        conn.rollback()
        print(f"Error adding event: {e}")

        return None
    
def get_all_events():
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn is None:
            return []

        cur = conn.cursor()

        query = "SELECT name, location, start_time, end_time, description FROM events;"
        cur.execute(query)
        events = cur.fetchall()

        if events is None:
            return []
        
        return events
    
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()