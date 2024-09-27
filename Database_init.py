import mysql.connector
from mysql.connector import Error
import hashlib
from Register_window import RegisterWindow

# Database configuration
db_config = {
    'user': 'root',       # Replace with your MySQL username
    'password': '',      # Replace with your MySQL password
    'host': 'localhost',
    'database': 'test',   # Replace with your database name
    'raise_on_warnings': True,
}

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(f'Error: {e}')

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Connection closed')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, department):
        if not self.connection or not self.connection.is_connected():
            print("Database connection is not established.")
            return

        cursor = self.connection.cursor()
        hashed_password = self.hash_password(password)

        try:
            # Insert the username and department into the usernames table
            cursor.execute('INSERT INTO usernames (username, departments) VALUES (%s, %s)', (username, department))
            user_id = cursor.lastrowid

            # Insert the hashed password into the passwords table
            cursor.execute('INSERT INTO passwords (user_id, password) VALUES (%s, %s)', (user_id, hashed_password))
            self.connection.commit()

            print(f'User {username} added successfully in {department}')
        except Error as e:
            print(f'Error: {e}')
        finally:
            cursor.close()

    def verify_user(self, username, password):
        if not self.connection or not self.connection.is_connected():
            print("Database connection is not established.")
            return False

        cursor = self.connection.cursor()
        hashed_password = self.hash_password(password)

        try:
            cursor.execute('''
                SELECT u.username, p.password
                FROM usernames u
                JOIN passwords p ON u.id = p.user_id
                WHERE u.username = %s AND p.password = %s
            ''', (username, hashed_password))
            return cursor.fetchone() is not None
        except Error as e:
            print(f'Error: {e}')
        finally:
            cursor.close()
        return False
