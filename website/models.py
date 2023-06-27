from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    properties = db.relationship('Property')


    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
class Property(db.Model, UserMixin):
    __tablename__ = 'properties' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    size = db.Column(db.Integer)
    location = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, size, location, user_id):
        self.name = name
        self.size = size
        self.location = location
        self.user_id = user_id