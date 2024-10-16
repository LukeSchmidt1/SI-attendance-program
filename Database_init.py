import mysql.connector
from mysql.connector import Error
import hashlib
from Register_window import RegisterWindow

# Database configuration
db_config = {
    'user': 'root',       # Replace with your MySQL username
    'password': '',      # Replace with your MySQL password
    'host': 'localhost',
    'database': 'test',   # Starting with the test database
    'raise_on_warnings': True,
}

class Database:
    def __init__(self):
        self.connection = None
        self.connect('test')  # Start with the test database

    def connect(self, database_name):
        # Set the database name in the config
        db_config['database'] = database_name  
        try:
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                print(f'Connected to {database_name} database')
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
            cursor.execute('INSERT INTO usernames (username, departments) VALUES (%s, %s)', (username, department))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO passwords (user_id, password) VALUES (%s, %s)', (user_id, hashed_password))
            self.connection.commit()
            print(f'User {username} added successfully in {department}')
        except Error as e:
            print(f'Error: {e}')
        finally:
            cursor.close()

    def switch_database(self, database_name):
        self.close()  # Close the existing connection
        self.connect(database_name)  # Connect to the new database

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
    
    def get_leaders(self):
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT first_name, last_name, class, session_days, session_times, room_location, observed_count, department
                FROM leaders
            """
            cursor.execute(query)
            leaders = cursor.fetchall()  # Fetch all the rows
            print(leaders)  # Debug print to see fetched data
            return leaders
        except Error as e:
            print(f'Error: {e}')
            return []
        finally:
            cursor.close()
