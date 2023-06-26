from flask import Blueprint, render_template, request, flash, redirect, url_for
import sqlite3
from .views import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email,))
        row = user.fetchone()
        if row is None:
            flash('User does not exist.', category='error')
        else:
            result_dict = dict(zip(row.keys(), row))

            user = User()
            user.id = result_dict['id']
            user.name = result_dict['name']
            user.email = result_dict['email']
            user.contact = result_dict['contact']
            user.password = result_dict['password']
 
            if check_password_hash(result_dict['password'], password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        conn.close()
    return render_template("login.html", user=current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data =request.form
    if request.method == 'POST':
        agency_name = request.form.get('agencyName')
        email = request.form.get('email')
        contact = request.form.get('contact')        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        conn = get_db_connection()
        table = conn.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name LIKE 'users';")
        row = table.fetchone()
        conn.close()
        if row is not None:
            table_dict = dict(zip(row.keys(), row))
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email,))
            row = user.fetchone()
            if row is not None:
                flash('Email already exists.', category='error')
            else:
                add_user(agency_name, email, contact, password1, password2)
        else:
            add_user(agency_name, email, contact, password1, password2)
            
    return render_template("sign_up.html")

def add_user(agency_name, email, contact, password1, password2):
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
        password = generate_password_hash(password1, method='scrypt')
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
        return redirect(url_for('.login'))
    return redirect(url_for('.sign_up'))
