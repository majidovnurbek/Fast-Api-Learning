import psycopg2
from psycopg2.extras import DictCursor

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.db_url)
        print("Database connected!")

    def create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            self.conn.commit()
            print("Table 'users' created successfully!")

    def add(self, user_id: int, full_name: str, username: str, email: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (user_id, full_name, username, email) VALUES (%s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING",
                (user_id, full_name, username, email)
            )
            self.conn.commit()

    def all(self) -> list[dict]:
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return [dict(user) for user in users]

    def is_exists(self, user_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)", (user_id,))
            return cursor.fetchone()[0]

    def update(self, user_id: int, new_name: str) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE users SET full_name = %s WHERE user_id = %s", (new_name, user_id))
            self.conn.commit()
            return cursor.rowcount

    def delete(self, user_id: int) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            self.conn.commit()
            return cursor.rowcount

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed!")
