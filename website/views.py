from flask import Blueprint, render_template, flash, redirect, request, current_app, redirect, url_for
import sqlite3
from flask_mail import Message, Mail
#from flask_login import login_required, current_user


views = Blueprint('views', __name__)

mail = Mail()


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

@views.route('/contact-us', methods=['GET', 'POST'])
#@login_required
def contact_us():
    #from . import login_manager

    if request.method == 'POST':
        #name = request.form['name']
        #email = current_user.email  # Get the email of the currently logged-in user
        #phone = request.form['phone']
        #subject = request.form['subject']
        #message = request.form['message']

        #mail.init_app(current_app)

        #msg = Message(
           # subject="New contact form submission - {}".format(subject),
          #  sender=email,
         #   recipients=['transcriberandwriter@gmail.com']
        #)

        #msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{message}"

        #mail.send(msg)

        flash('Thank you for your message. We will get back to you shortly.')

        return redirect(url_for('views.home'))

    return render_template("contact.html")