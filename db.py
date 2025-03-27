import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from the correct path
env_path = Path('.') / '.env'
load_dotenv(env_path)

def get_db_connection():
    try:
        # Print environment variables for debugging
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_pass = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'user_registration')
        
        print(f"Attempting to connect with: HOST={db_host}, USER={db_user}, DB={db_name}")
        
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            return connection
        else:
            print("Failed to connect to MySQL database")
            return None
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(query, params=None, fetch_one=False):
    connection = get_db_connection()
    if not connection:
        print("No database connection available")
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        print(f"Executing query: {query}")
        print(f"With parameters: {params}")
        
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
            print(f"Query affected {cursor.rowcount} rows")
            print(f"Last insert ID: {result}")
            
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Parameters: {params}")
        if not query.strip().upper().startswith('SELECT'):
            connection.rollback()
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("Database connection closed")