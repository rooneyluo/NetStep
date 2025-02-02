from db_config import db_config  # Configuration for database connection
from database_connection_manager import DatabaseConnectionManager


# create users table
def create_users_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'organizer', 'admin', 'superadmin')),
            is_email_verified BOOLEAN DEFAULT FALSE,
            email_verified_at TIMESTAMP,
            phone_number VARCHAR(20),
            is_phone_verified BOOLEAN DEFAULT FALSE,
            phone_verified_at TIMESTAMP,
            photo BYTEA,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(10) CHECK (status IN ('active', 'inactive')),
            likes INT DEFAULT 0,
            dislikes INT DEFAULT 0,
            created_by INT,
            updated_by INT,
            CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
            CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
            CONSTRAINT chk_likes CHECK (likes >= 0),
            CONSTRAINT chk_dislikes CHECK (dislikes >= 0),
            CONSTRAINT chk_email_verified CHECK (is_email_verified = FALSE OR email_verified_at IS NOT NULL),
            CONSTRAINT chk_phone_verified CHECK (is_phone_verified = FALSE OR phone_verified_at IS NOT NULL)
        );
    """)
    print("Users table created successfully!")
# Create events table
def create_events_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            organizer_id INT NOT NULL,
            location_id INT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INT NOT NULL,
            updated_by INT NOT NULL,
            current_participants INT DEFAULT 0,
            max_participants INT DEFAULT 0,
            status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'completed', 'expired')),
            tags VARCHAR(255) DEFAULT '{}',
            likes INT DEFAULT 0,
            dislikes INT DEFAULT 0,   
            CONSTRAINT fk_organizer FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
            CONSTRAINT fk_user_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_user_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT chk_max_participants CHECK (max_participants >= 0),
            CONSTRAINT chk_current_participants CHECK (current_participants >= 0),
            CONSTRAINT chk_likes CHECK (likes >= 0),
            CONSTRAINT chk_dislikes CHECK (dislikes >= 0)
        );
    """)
    print("Events table created successfully!")
# Create locations table
def create_locations_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            information VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INT NOT NULL,
            updated_by INT NOT NULL,
            status VARCHAR(10) DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
            CONSTRAINT fk_user_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_user_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("Locations table created successfully!")
# Create event_participants table
def create_event_participants_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_participants (
            event_id INT NOT NULL,
            participant_id INT NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('pending', 'approved', 'rejected', 'waiting', 'cancelled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_by INT NOT NULL,
            CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            CONSTRAINT fk_participant FOREIGN KEY (participant_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
            CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
            CONSTRAINT pk_event_participant PRIMARY KEY (event_id, participant_id)
        );
    """)
    print("Event participants table created successfully!")
# Create event_feedbacks table
def create_event_feedbacks_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_feedbacks (
            id SERIAL PRIMARY KEY,
            event_id INT NOT NULL,
            user_id INT NOT NULL,
            comment TEXT,
            like_dislike BOOLEAN,  -- TRUE for like, FALSE for dislike
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("Event feedbacks table created successfully!")
# Create user_feedbacks table
def create_user_feedbacks_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_feedbacks (
            id SERIAL PRIMARY KEY,
            event_id INT NOT NULL,
            user_id INT NOT NULL,
            organizer_id INT NOT NULL,
            comment TEXT,
            like_dislike BOOLEAN,  -- TRUE for like, FALSE for dislike
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_organizer FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User feedbacks table created successfully!")
# Create user_notifications table
def create_user_notifications_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_notifications (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            type VARCHAR(50) NOT NULL CHECK (type IN ('message', 'event_status_changed', 'system')),
            message TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User notifications table created successfully!")
# Create user_messages table
def create_user_messages_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_messages (
            id SERIAL PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            message TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User messages table created successfully!")
# Create login_attempts table
def create_login_attempts_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            ip_address VARCHAR(50) NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            location VARCHAR(255),
            user_agent VARCHAR(255),
            status VARCHAR(10) DEFAULT 'success' CHECK (status IN ('success', 'failed')),
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("Login attempts table created successfully!")
# Create user_auth_providers table
def create_user_auth_providers_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_auth_providers (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            provider VARCHAR(50) NOT NULL CHECK (provider IN ('google', 'line')),
            provider_id VARCHAR(255) NOT NULL,
            provider_token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User auth providers table created successfully!")
# Create user_tokens table
def create_user_tokens_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_tokens (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) NOT NULL,
            token_expire TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User tokens table created successfully!")
# Create user_verification_codes table
def create_user_verification_codes_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_verification_codes (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            code VARCHAR(50) NOT NULL,
            code_type VARCHAR(50) NOT NULL CHECK (code_type IN ('email', 'phone')),
            code_expire TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("User verification codes table created successfully!")
# create database
def create_database(database_name):
    try:
        new_db_config = db_config.copy()
        new_db_config['dbname'] = 'postgres'  # Connect to the default database to create a new one

        with DatabaseConnectionManager(new_db_config) as conn:
            with conn.cursor() as cur:
                conn.autocommit = True

                cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}';")
                exists = cur.fetchone()
                if exists:
                    print(f"Database {database_name} already exists!")
                    return
                
                # Validate database name
                if not database_name.isidentifier():
                    raise ValueError("Invalid database name: must contain only letters, numbers, or underscores, and cannot start with a number")
                    
                cur.execute(f"CREATE DATABASE {database_name};")
                print(f"Database {database_name} created successfully!")

    except Exception as e:
        print(f"Error creating database: {e}")        
# Function to create tables
def create_tables():
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                # Create tables
                create_users_table(cur)
                create_locations_table(cur)
                create_events_table(cur)
                create_event_participants_table(cur)
                create_event_feedbacks_table(cur)
                create_user_feedbacks_table(cur)
                create_user_notifications_table(cur)
                create_user_messages_table(cur)
                create_login_attempts_table(cur)
                create_user_auth_providers_table(cur)
                create_user_tokens_table(cur)
                create_user_verification_codes_table(cur)
            
                # Commit changes
                conn.commit()
                print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
# Function to drop tables
def drop_tables():
    try:
        with DatabaseConnectionManager(db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS user_verification_codes;")
                cur.execute("DROP TABLE IF EXISTS user_tokens;")
                cur.execute("DROP TABLE IF EXISTS user_auth_providers;")
                cur.execute("DROP TABLE IF EXISTS login_attempts;")
                cur.execute("DROP TABLE IF EXISTS user_messages;")
                cur.execute("DROP TABLE IF EXISTS user_notifications;")
                cur.execute("DROP TABLE IF EXISTS user_feedbacks;")
                cur.execute("DROP TABLE IF EXISTS event_feedbacks;")
                cur.execute("DROP TABLE IF EXISTS event_participants;")
                cur.execute("DROP TABLE IF EXISTS events;")
                cur.execute("DROP TABLE IF EXISTS locations;")
                cur.execute("DROP TABLE IF EXISTS users;")
                conn.commit()
                print("Tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")

if __name__ == "__main__":
    #drop_tables()
    create_database("net_step")
    create_tables()