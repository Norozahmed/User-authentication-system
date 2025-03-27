import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from the correct path
env_path = Path('.') / '.env'
load_dotenv(env_path)

def test_connection():
    try:
        # First try to connect without database to create it if needed
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS user_registration")
            print("Database 'user_registration' created or already exists")
            
            # Switch to the database
            cursor.execute("USE user_registration")
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    verification_code VARCHAR(32),
                    is_verified TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reset_token VARCHAR(32),
                    reset_token_expiry DATETIME,
                    full_name VARCHAR(100),
                    bio TEXT,
                    skills VARCHAR(255),
                    profile_pic VARCHAR(255)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """)
            print("Users table created or already exists")
            
            # Test insert
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES ('test_user', 'test@example.com', 'test_password')
                ON DUPLICATE KEY UPDATE username=username
            """)
            connection.commit()
            print("Test insert successful")
            
            # Test select
            cursor.execute("SELECT * FROM users WHERE email='test@example.com'")
            result = cursor.fetchone()
            if result:
                print("Test select successful")
            
            print("All database tests passed!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    test_connection() 