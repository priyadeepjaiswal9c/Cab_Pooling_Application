import hashlib

class AuthController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, email=None, phone=None):
        hashed_password = self.hash_password(password)
        
        cursor = self.db_manager.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                (username, hashed_password, email, phone)
            )
            self.db_manager.conn.commit()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"

    def login_user(self, username, password):
        hashed_password = self.hash_password(password)
        
        cursor = self.db_manager.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed_password)
        )
        
        user_row = cursor.fetchone()
        if user_row:
            return True, user_row  # Return user data on success
        else:
            return False, "Invalid username or password"

    def get_user_contact(self, user_id):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT username, email, phone 
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        return cursor.fetchone()
