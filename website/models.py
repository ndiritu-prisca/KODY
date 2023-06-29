from . import db
from flask_login import UserMixin
import json


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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'contact': self.contact,
            'password': self.password
        }

    def __str__(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, json_data):
        user_data = json.loads(json_data)
        user = cls()
        user.id = user_data['id']
        user.name = user_data['name']
        user.email = user_data['email']
        user.contact = user_data['contact']
        user.password = user_data['password']
        return user



class Property(db.Model, UserMixin):
    __tablename__ = 'properties' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    bd = db.Column(db.Integer)
    location = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='property', cascade='all, delete')

    def __init__(self, name, bd, location, user_id, images):
        self.name = name
        self.bd = bd
        self.location = location
        self.user_id = user_id
        self.images = images
    
class Image(db.Model, UserMixin):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))