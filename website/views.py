from flask import Blueprint, render_template, flash, redirect, request, current_app, redirect, url_for
import sqlite3
from flask_mail import Message, Mail
from flask_login import login_required, current_user
from .models import Property
from . import db
from flask import jsonify


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
    if request.method == "GET":
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


@views.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    user_properties = conn.execute('SELECT * FROM properties WHERE user_id = ?', (current_user.id,)).fetchall()
    conn.close()
    return render_template("profile.html", user_properties=user_properties)

@views.route('/profile/create', methods=['GET', 'POST'])
@login_required
def add_properties():
    if request.method == "POST":
        name = request.form.get('propertyName')
        bd = request.form.get('bd')
        location = request.form.get('location')
        conn = get_db_connection()
        conn.execute('INSERT INTO properties (name, bd, location, user_id) VALUES (?, ?, ?, ?)',
                    (name, bd, location, current_user.id))
        conn.commit()
        conn.close()

        flash('Property added successfully!', category='success')
        return redirect(url_for(".profile"))
    return render_template("create_properties.html")

@views.route('/profile/1', methods=['GET'])
@login_required
def property_item():
    conn = get_db_connection()
    property_item = conn.execute('SELECT * FROM properties WHERE id = ?',
                    ())
    conn.commit()
    conn.close()
    return render_template("property_item.html", property_item=property_item)



@views.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_properties(id):
    if request.method == "POST":
        name = request.form.get('propertyName')
        bd = request.form.get('bd')
        location = request.form.get('location')
        conn = get_db_connection()
        conn.execute('UPDATE properties SET (name, bd, location, user_id) VALUES (?, ?, ?, ?) WHERE id = ?',
                    (name, bd, location, current_user.id, id))
        conn.commit()
        conn.close()

        flash('Property added successfully!', category='success')
        return redirect(url_for(".profile"))
    conn = get_db_connection()
    property_details = conn.execute('SELECT * FROM properties WHERE id = ?',
                    (id))
    conn.commit()
    conn.close()
    return render_template("edit_properties.html")