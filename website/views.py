from flask import Blueprint, render_template
import sqlite3


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

@views.route('/about')
def about():
  return render_template("about.html")

@views.route('/contact-us')
def contact_us():
  return render_template("contact.html")
