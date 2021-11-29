#import app.__init__ 
from app import db, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)