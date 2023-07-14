""" Module handles app initialization """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, urandom
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = 'website/static/uploads/'

def create_app():
    """ Creates the app """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com' #app config for flask mail implementation
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'kodyapp@yahoo.com'
    app.config['MAIL_PASSWORD'] = '@KDYapp1'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_db(app)

    login = LoginManager()
    login.login_view = 'auth.login'
    login.init_app(app)

    from .views import get_db_connection
    @login.user_loader
    def load_user(user_id):
        """ Loads the user """
        userId = int(user_id)
        conn = get_db_connection() #Connecting to the db
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = user.fetchone()
        if row is None:
            flash('No user.', category='error')
        else:
            result_dict = dict(zip(row.keys(), row))
            user = User()
            user.id = result_dict['id']
            user.name = result_dict['name']
            user.email = result_dict['email']
            user.contact = result_dict['contact']
            user.password = result_dict['password']
        conn.close()
        return user

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("created database")
