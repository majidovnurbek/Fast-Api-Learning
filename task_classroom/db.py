import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(".env")

conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cursor = conn.cursor()  # creating a cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS users
(
    id serial PRIMARY KEY NOT NULL,
    fullname VARCHAR(255)  NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")


class Database:
    def __init__(self, db_file, user, password, host, port):
        self.connection = psycopg2.connect(database=db_file, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

    def add_user(self, full_name, username, email, password):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)',
                                       (full_name, username, email, password))

    def update_user(self, id,  full_name, username, email, password):
        with self.connection:
            return self.cursor.execute('UPDATE users SET fullname=%s, username=%s, email=%s, password=%s WHERE id=%s',
                                       (full_name,username, email, password, id))

    def get_users(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()

    def delete_users(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE id = %s", (id,))

    def check_user(self, username):
        with self.connection:
            self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            return self.cursor.fetchone()

conn.commit()
conn.close()

