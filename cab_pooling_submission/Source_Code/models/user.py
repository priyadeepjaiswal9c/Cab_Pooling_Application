class User:
    def __init__(self, id, username, email=None, phone=None):
        self.id = id
        self.username = username
        self.email = email
        self.phone = phone

    @staticmethod
    def from_row(row):
        return User(row['id'], row['username'], row['email'], row['phone'])
