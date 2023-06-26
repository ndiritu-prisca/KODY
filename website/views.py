from flask import Blueprint, render_template
import sqlite3
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@views.route('/')
def home():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template("home.html", users=users)

@views.route('/aboutUs')
def aboutUs():
    return render_template("aboutUs.html")

@views.route('/properties')
def properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()
    conn.close()
    return render_template("properties.html", properties=properties)

@views.route('/agents')
def agents():
    return render_template("agents.html")

@views.route('/contactUs')
def contactUs():
    return render_template("contactUs.html")
