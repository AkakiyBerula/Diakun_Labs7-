from .. import db, SQLAlchemy, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    about_me = db.Column(db.Text, nullable=True)

    contracts = db.relationship('Contracts', backref='contracts_activities', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __init__(self, username, email, password, image_file = "default.jpg", about_me = ''):
        self.username = username
        self.email = email
        self.about_me = about_me
        self.image_file = image_file
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)