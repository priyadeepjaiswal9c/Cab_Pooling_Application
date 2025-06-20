import sqlite3
from database.schema import create_tables

class DatabaseManager:
    def __init__(self, db_path="cab_pooling.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        create_tables(self.conn)

    def close(self):
        self.conn.close()
