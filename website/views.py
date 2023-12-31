""" Modules holds all the routes """
from flask import Blueprint, render_template, flash, redirect, request, current_app, redirect, url_for, send_from_directory
import sqlite3
from flask_mail import Message, Mail
from flask_login import login_required, current_user
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def get_db_connection():
    """ Initializes db connection """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """ Checks whether the image file type is among the allowed extentions """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    """ Renders the home page """
    if request.method == "GET":
        conn = get_db_connection()
        properties = conn.execute('SELECT * FROM properties ORDER BY id DESC LIMIT 3').fetchall()
        file_dict = {}
        # Iterate through each row in user_properties
        for row in properties:
            property_id = row['id']

            agency = conn.execute('SELECT name, contact FROM users WHERE id = ?', (row['user_id'],)).fetchone()
            agency_name, contact = agency['name'], agency['contact'] if agency else None
    
            # Retrieve filenames from the images table for the current property_id
            images = conn.execute('SELECT filename FROM images WHERE property_id = ?', (property_id,)).fetchall()
        
            # Extract the filenames from the result set
            filenames = [image['filename'] for image in images]
        
            # Assign the filenames to the property_id in the dictionary
            file_dict[property_id] = {'filenames': filenames, 'agency_name': agency_name, 'contact': contact}
    return render_template("home.html", properties=properties, files=file_dict)

@views.route('/aboutUs')
def aboutUs():
    """ Renders the about page """
    return render_template("about.html")

@views.route('/properties', methods=['GET'])
def properties():
    """ Renders the properties page """
    if request.method == "GET":
        conn = get_db_connection()
        properties = conn.execute('SELECT * FROM properties').fetchall()
        file_dict = {}
        # Iterate through each row in user_properties
        for row in properties:
            property_id = row['id']

            agency = conn.execute('SELECT name, contact FROM users WHERE id = ?', (row['user_id'],)).fetchone()
            agency_name, contact = agency['name'], agency['contact'] if agency else None
    
            # Retrieve filenames from the images table for the current property_id
            images = conn.execute('SELECT filename FROM images WHERE property_id = ?', (property_id,)).fetchall()
        
            # Extract the filenames from the result set
            filenames = [image['filename'] for image in images]
        
            # Assign the filenames to the property_id in the dictionary
            file_dict[property_id] = {'filenames': filenames, 'agency_name': agency_name, 'contact': contact}
        conn.close()
        return render_template("properties.html", properties=properties, files=file_dict)

@views.route('/agents')
def agents():
    """ Renders the agents page """
    conn = get_db_connection()
    query = '''
        SELECT users.id, users.name, users.contact, bios.filename, bios.description
        FROM users
        LEFT JOIN bios ON users.id = bios.user_id
    '''
    agents = conn.execute(query).fetchall()
    conn.close()
    return render_template("agents.html", agents=agents)

@views.route('/agent/<id>')
def agent(id):
    """ Renders the specific agent page """
    conn = get_db_connection()
    agent_properties = conn.execute('SELECT * FROM properties WHERE user_id = ?', (id,)).fetchall()
    agent = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    file_dict = {}
    # Iterate through each row in user_properties
    for row in agent_properties:
        property_id = row['id']
    
        # Retrieve filenames from the images table for the current property_id
        images = conn.execute('SELECT filename FROM images WHERE property_id = ?', (property_id,)).fetchall()
    
        # Extract the filenames from the result set
        filenames = [image['filename'] for image in images]
    
        # Assign the filenames to the property_id in the dictionary
        file_dict[property_id] = filenames

    conn.close()
    return render_template("agent_properties.html", agent_properties=agent_properties, files=file_dict, agent=agent)

@views.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    """ Renders the contact page """

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        mail = Mail(current_app)
        mail.init_app(current_app)

        msg = Message(
            subject="New contact form submission - {}".format(subject),
            sender="kodyapp@yahoo.com",
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


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """ Renders the profile page once user is logged in"""
    if request.method == 'POST':
        description = request.form.get('description')
        conn = get_db_connection()
        desc = conn.execute('SELECT * FROM bios WHERE user_id = ?', (current_user.id,)).fetchone()
        if desc is not None:
                conn.execute('UPDATE bios SET description = ? WHERE user_id = ?', (description, current_user.id))
        else:
            conn.execute(
                'INSERT INTO bios (description, user_id) VALUES (?, ?)',
                (description, current_user.id)
            )
        conn.commit()
        conn.close()
    conn = get_db_connection()
    user_properties = conn.execute('SELECT * FROM properties WHERE user_id = ?', (current_user.id,)).fetchall()
    file_dict = {}
    # Iterate through each row in user_properties
    for row in user_properties:
        property_id = row['id']
    
        # Retrieve filenames from the images table for the current property_id
        images = conn.execute('SELECT filename FROM images WHERE property_id = ?', (property_id,)).fetchall()
    
        # Extract the filenames from the result set
        filenames = [image['filename'] for image in images]
    
        # Assign the filenames to the property_id in the dictionary
        file_dict[property_id] = filenames

    profile_pic = conn.execute('SELECT * FROM bios WHERE user_id = ?', (current_user.id,)).fetchone()
    conn.close()
    return render_template("profile.html", user_properties=user_properties, files=file_dict, pic=profile_pic)

@views.route('/details/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Handles profile editing """
    if request.method == "POST":
        agency_name = request.form.get('agencyName')
        email = request.form.get('email')
        contact = request.form.get('contact')   
        conn = get_db_connection()
        conn.execute('UPDATE users SET name = ?, email = ?, contact = ? WHERE id = ?',
              (agency_name, email, contact, current_user.id))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!', category='success')
        return redirect(url_for(".profile"))
    conn = get_db_connection()
    dataobj = conn.execute('SELECT * FROM users WHERE id = ?',
                    (current_user.id,)).fetchone()
    
    data = dict(zip(dataobj.keys(), dataobj))
    conn.commit()
    conn.close()
    return render_template("edit_profile.html", data=data)

@views.route('/profile/create', methods=['GET', 'POST'])
@login_required
def add_properties():
    """ Handles addition of properties page"""
    if request.method == "POST":
        name = request.form.get('propertyName')
        bd = request.form.get('bd')
        location = request.form.get('location')
        price = request.form.get('price')
        conn = get_db_connection()
        created_property = conn.execute('INSERT INTO properties (name, bd, location, price, user_id) VALUES (?, ?, ?, ?, ?)',
                    (name, bd, location, price, current_user.id))
        property_id = created_property.lastrowid
        conn.commit()
        conn.close()

        flash('Property added successfully!', category='success')
        flash('upload property images!', category='request')
        return redirect(url_for("views.upload_image", property_id=property_id))
    return render_template("create_properties.html")


@views.route('/upload/<property_id>', methods=['GET', 'POST'])
def upload_image(property_id):
    """ Handles property's images upload page """
    if request.method == 'POST':
        if 'images[]' not in request.files:
            flash("No image(s) uploaded. Image must be 'png', 'jpg', or 'jpeg'")
        files = request.files.getlist('images[]')

        for file in files:
            if file and allowed_file(file.filename):
                # Save the image to a folder on your server
                filename = secure_filename(file.filename)
                from . import create_app
                app = create_app()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Create a new Image instance and associate it with the property
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO images (filename, property_id) VALUES (?, ?)',
                    (filename, property_id)
                )
                conn.commit()
                conn.close()
        return redirect(url_for("views.profile"))
    return render_template("upload.html", property_id=property_id)

@views.route('/profile/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_properties(id):
    """ Handles property editing """
    if request.method == "POST":
        name = request.form.get('propertyName')
        bd = request.form.get('bd')
        location = request.form.get('location')
        price = request.form.get('price')
        conn = get_db_connection()
        conn.execute('UPDATE properties SET name = ?, bd = ?, location = ?, price = ?, user_id = ? WHERE id = ?',
              (name, bd, location, price, current_user.id, id))
        conn.commit()
        conn.close()

        flash('Property edited successfully!', category='success')
        return redirect(url_for(".profile"))
    conn = get_db_connection()
    dataobj = conn.execute('SELECT * FROM properties WHERE id = ?',
                    (id,)).fetchone()
    
    data = dict(zip(dataobj.keys(), dataobj))
    conn.commit()
    conn.close()
    return render_template("edit_properties.html", data=data)

@views.route('/profile/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_properties(id):
    """ Handles deletion of property """
    conn = get_db_connection()
    conn.execute('DELETE FROM properties WHERE id = ?',
                    (id,))
    conn.commit()
    conn.close()

    flash('Property deleted successfully!', category='success')
    return redirect(url_for(".profile"))

@views.route('/upload_pic/<id>', methods=['GET', 'POST'])
@login_required
def upload_pic(id):
    """ Handles profile picture upload """
    if request.method == 'POST':
        if 'image' not in request.files:
            flash("No image uploaded. Image must be 'png', 'jpg', or 'jpeg'")
        file = request.files['image']

        if file and allowed_file(file.filename):
            # Save the image to a folder on your server
            filename = secure_filename(file.filename)
            from . import create_app
            app = create_app()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create a new Image instance and associate it with the property
            conn = get_db_connection()
            profile_pic = conn.execute('SELECT * FROM bios WHERE user_id = ?', (current_user.id,)).fetchone()
            if profile_pic is not None:
                conn.execute('UPDATE bios SET filename = ? WHERE user_id = ?', (filename, current_user.id))
            else:
                conn.execute(
                    'INSERT INTO bios (filename, user_id) VALUES (?, ?)',
                    (filename, id)
                )
            conn.commit()
            conn.close()
    return redirect(url_for("views.profile"))
