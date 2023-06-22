from flask import Blueprint, render_template, request, flash
import sqlite3
from .views import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")
    
@auth.route('/logout')
def logout():
    return render_template("logout.html")
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data =request.form
    print(data)
    if request.method == 'POST':
        agency_name = request.form.get('agencyName')
        email = request.form.get('email')
        contact = request.form.get('contact')        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(agency_name) < 2:
            flash('Agency name must be greater than 1 characters.', category='error')
        elif len(email) < 11:
            flash('Agency email must be greater than 10 characters.', category='error')
        elif len(contact) < 9:
            flash('Phone number must be greater than 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            password = generate_password_hash(password1, method='sha256')
            conn = get_db_connection()
            conn.execute('CREATE TABLE IF NOT EXISTS users ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name STRING(150) UNIQUE,'
                'email STRING(150) UNIQUE,'
                'contact INTEGER UNIQUE,'
                'password STRING(150)'
                ');'
            )
            conn.commit()
            conn.execute('INSERT INTO users (name, email, contact, password) VALUES (?, ?, ?, ?)',
                         (agency_name, email, contact, password))
            conn.commit()
            conn.close()
            flash('Account created successfully!', category='success')
    return render_template("sign_up.html")