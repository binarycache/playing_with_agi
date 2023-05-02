import sqlite3

class UserDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                diet_plan TEXT
            )
        """)
        self.conn.commit()

    def add_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def user_exists(self, username):
        self.cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone() is not None

    def validate_user(self, username, password):
        self.cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def update_diet_plan(self, username, diet_plan):
        self.cursor.execute("UPDATE users SET diet_plan = ? WHERE username = ?", (diet_plan, username))
        self.conn.commit()

    def get_user_diet_plan(self, username):
        self.cursor.execute("SELECT diet_plan FROM users WHERE username = ?", (username,))
        diet_plan = self.cursor.fetchone()
        return diet_plan[0] if diet_plan is not None else None

    def close(self):
        self.conn.close()
