""" module handles the data models """
from . import db
from flask_login import UserMixin
import json


class User(db.Model, UserMixin):
    """ 
    User class inherit from db.Model and UserMixin
    db.Model allow connection with the db
    UserMixin allow implementation of flask_login 
    """
    
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    properties = db.relationship('Property')
    bios = db.relationship('Bio')

    def get_id(self):
        """ 
        Method gets the user id
        args:
            self
        return (str):
            user id
        """
        return str(self.id)

    def is_active(self):
        """ Check user is loaded """
        return True

    def is_authenticated(self):
        """ check user is authenticated """
        return True

    def is_anonymous(self):
        """ restrict login """
        return False

class Property(db.Model, UserMixin):
    """ representation of Property model """
    __tablename__ = 'properties' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    bd = db.Column(db.Integer)
    location = db.Column(db.String(150))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='property', cascade='all, delete')

    def __init__(self, name, bd, location, user_id, images):
        """ Initializes property """
        self.name = name
        self.bd = bd
        self.location = location
        self.user_id = user_id
        self.images = images
    
class Image(db.Model, UserMixin):
    """ Representation of Image model """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

class Bio(db.Model, UserMixin):
    """ Representations of Bio model """
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
