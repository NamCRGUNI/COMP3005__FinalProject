import psycopg2

# Database connection details
DB_HOST = "localhost"
DB_NAME = "NewFitnessClub"
DB_USER = "usr1"
DB_PASSWORD = "pwd1!@#$"


def create_connection():
    """
    Create a connection to the PostgreSQL database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

def close_connection(conn):
    """
    Close the database connection.
    """
    if conn:
        conn.close()
        

def execute_query(query, params=None):
    """
    Execute a SQL query with optional parameters.
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            cur.close()
            close_connection(conn)
    else:
        print("Failed to establish database connection.")
def fetch_data(query, params=None):
    """
    Fetch data from the database using a SQL query with optional parameters.
    """
    conn = create_connection()
    data = None
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            data = cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            cur.close()
            close_connection(conn)  # Move the close_connection call here
    else:
        print("Failed to establish database connection.")
    return data
