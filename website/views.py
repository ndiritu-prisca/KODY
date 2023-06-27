from flask import Blueprint, render_template, flash, redirect, request, current_app, redirect, url_for
import sqlite3
from flask_mail import Message, Mail
from flask_login import login_required, current_user
from .models import Property
from . import db
 

views = Blueprint('views', __name__)

mail = Mail()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@views.route('/')
def home():
    # conn = get_db_connection()
    # users = conn.execute('SELECT * FROM users').fetchall()
    # conn.close()
    return render_template("home.html")

@views.route('/aboutUs')
def aboutUs():
    return render_template("about.html")

@views.route('/properties', methods=['GET'])
def properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()
    conn.close()
    return render_template("properties.html", properties=properties)

@views.route('/agents')
def agents():
    conn = get_db_connection()
    agents = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template("agents.html", agents=agents)


@views.route('/contactUs', methods=['GET', 'POST'])
def contactUs():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        mail.init_app(current_app)

        msg = Message(
            subject="New contact form submission - {}".format(subject),
            sender=email,
            recipients=['transcriberandwriter@gmail.com']
        )

        msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{message}"

        try:
            mail.send(msg)
            flash('Thank you for your message. We will get back to you shortly.')

        except Exception as e:
            flash('An error occurred while sending the message. Please try again later.')
        return redirect(url_for('views.home'))

    return render_template("contact.html")


from . import create_app
@views.route('/profile')
@login_required
def profile():
    user_properties = Property.query.filter_by(user_id=current_user.id).all()
    print(user_properties)
    return render_template("profile.html")

@views.route('/properties', methods=['POST'])
@login_required
def add_properties():
    name = request.form.get('propertyName')
    size = request.form.get('size')
    location = request.form.get('location')        
    property = Property(name=name, size=size, location=location, user_id=current_user.id)
    db.session.add(property)
    db.session.commit()
    
    flash('Property added successfully!', category='success')
    return redirect(url_for('.profile'))