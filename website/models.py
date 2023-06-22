from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    properties = db.relationship('Property')

class Property(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    size = db.Column(db.Integer, unique=True)
    user_id = (db.Integer, db.ForeignKey('user.id'))