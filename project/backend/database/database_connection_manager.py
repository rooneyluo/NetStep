import psycopg2

# Database connection manager
class DatabaseConnectionManager:
    def __init__(self, db_config):
        self.conn = None
        self.db_config = db_config

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                dbname=self.db_config['dbname'],
                port=self.db_config['port']
            )
            return self.conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()