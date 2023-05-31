from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False

    def get_id(self):
        return self.username

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(username):
        # This is where you can implement fetching from a real data source
        # For now, we'll use a hardcoded user for demonstration
        if username == "admin":
            password_hash = generate_password_hash("admin123")  # plain password: admin123
            return User(username, password_hash)
        return None
