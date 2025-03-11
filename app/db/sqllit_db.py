import sqlite3


class Connection:
	def __init__(self, db_name="chat.db"):
		self.connection = sqlite3.connect(db_name, check_same_thread=False)
		self.cursor = self.connection.cursor()
		self.create_tables()

	def create_tables(self):
		self.cursor.execute("PRAGMA foreign_keys = ON;")
		self.cursor.execute(
			"""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
		)
		self.cursor.execute(
			"""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            message TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
		)
		self.connection.commit()

	def close(self):
		self.connection.close()
