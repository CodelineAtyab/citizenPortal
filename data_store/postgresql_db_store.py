import psycopg2
from typing import List, Optional
from dto import User
from app_logger import getLogger

module_logger = getLogger()

# Database connection parameters
DB_CONFIG = {
    "dbname": "appdb",
    "user": "d3user",
    "password": "d3pass",
    "host": "db",
    "port": "5432"
}


def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        module_logger.error(f"Failed to connect to database: {e}")
        raise


def get_db():
    """Dependency function for FastAPI to inject database connections."""
    conn = None
    try:
        conn = get_connection()
        module_logger.debug("Database connection established")
        yield conn
    except Exception as e:
        module_logger.error(f"Database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            module_logger.debug("Database connection closed")


def create_users_table():
    """Create the users table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        contact_no VARCHAR(20) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                module_logger.info("Users table created or already exists.")
    except Exception as e:
        module_logger.error(f"Error creating users table: {e}")
        raise


def create_user(user: User, conn=None) -> bool:
    """Insert a new user into the database."""
    insert_query = """
    INSERT INTO users (name, email, contact_no)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    
    try:
        if conn:
            # Use provided connection (for dependency injection)
            with conn.cursor() as cur:
                cur.execute(insert_query, (user.name, user.email, user.contact_no))
                user_id = cur.fetchone()[0]
                conn.commit()
                module_logger.info(f"User created successfully with ID: {user_id}")
                return True
        else:
            # Create new connection (for standalone usage)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (user.name, user.email, user.contact_no))
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    module_logger.info(f"User created successfully with ID: {user_id}")
                    return True
    except psycopg2.errors.UniqueViolation:
        module_logger.warning(f"User with email {user.email} or contact_no {user.contact_no} already exists.")
        return False
    except Exception as e:
        module_logger.error(f"Error creating user: {e}")
        raise


def get_all_users(conn=None) -> List[User]:
    """Retrieve all users from the database."""
    select_query = "SELECT name, email, contact_no FROM users ORDER BY id;"
    
    try:
        if conn:
            # Use provided connection (for dependency injection)
            with conn.cursor() as cur:
                cur.execute(select_query)
                rows = cur.fetchall()
                users = [User(name=row[0], email=row[1], contact_no=row[2]) for row in rows]
                module_logger.info(f"Retrieved {len(users)} users from database.")
                return users
        else:
            # Create new connection (for standalone usage)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(select_query)
                    rows = cur.fetchall()
                    users = [User(name=row[0], email=row[1], contact_no=row[2]) for row in rows]
                    module_logger.info(f"Retrieved {len(users)} users from database.")
                    return users
    except Exception as e:
        module_logger.error(f"Error retrieving users: {e}")
        raise


def get_user_by_contact_no(contact_no: str, conn=None) -> Optional[User]:
    """Retrieve a specific user by contact number."""
    select_query = "SELECT name, email, contact_no FROM users WHERE contact_no = %s;"
    
    try:
        if conn:
            # Use provided connection (for dependency injection)
            with conn.cursor() as cur:
                cur.execute(select_query, (contact_no,))
                row = cur.fetchone()
                if row:
                    user = User(name=row[0], email=row[1], contact_no=row[2])
                    module_logger.info(f"Found user with contact_no: {contact_no}")
                    return user
                else:
                    module_logger.info(f"No user found with contact_no: {contact_no}")
                    return None
        else:
            # Create new connection (for standalone usage)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(select_query, (contact_no,))
                    row = cur.fetchone()
                    if row:
                        user = User(name=row[0], email=row[1], contact_no=row[2])
                        module_logger.info(f"Found user with contact_no: {contact_no}")
                        return user
                    else:
                        module_logger.info(f"No user found with contact_no: {contact_no}")
                        return None
    except Exception as e:
        module_logger.error(f"Error retrieving user by contact_no: {e}")
        raise


def initialize_db_with_sample_data():
    """Create table and populate with sample data from in_memory_store."""
    from data_store.in_memory_store import temp_user_store
    
    try:
        create_users_table()
        
        # Insert sample users
        for user in temp_user_store:
            create_user(user)
        
        module_logger.info("Database initialized with sample data.")
    except Exception as e:
        module_logger.error(f"Error initializing database: {e}")
        raise


def delete_user_by_contact_no(contact_no: str) -> bool:
    """Delete a user by contact number."""
    delete_query = "DELETE FROM users WHERE contact_no = %s RETURNING id;"
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(delete_query, (contact_no,))
                result = cur.fetchone()
                conn.commit()
                if result:
                    module_logger.info(f"User with contact_no {contact_no} deleted successfully.")
                    return True
                else:
                    module_logger.info(f"No user found with contact_no: {contact_no}")
                    return False
    except Exception as e:
        module_logger.error(f"Error deleting user: {e}")
        raise


if __name__ == "__main__":
    # Test the database functions
    module_logger.info("Testing PostgreSQL database store...")
    
    try:
        # Initialize database with sample data
        initialize_db_with_sample_data()
        
        # Retrieve all users
        all_users = get_all_users()
        module_logger.info(f"All users: {all_users}")
        
        # Get specific user
        user = get_user_by_contact_no("12345678")
        if user:
            module_logger.info(f"Found user: {user}")
        
    except Exception as e:
        module_logger.error(f"Test failed: {e}")
