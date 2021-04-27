from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from flask_mail import Mail, Message
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"
MAIL_USERNAME = 'tofutang35728@gmail.com'
def create_app():
    app = Flask(__name__,static_url_path='')
    app.config['SECRET_KEY'] = "RandomString"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = 'Momin35728'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)

    from .views import views
    from .auth import auth
    from ._security_test import security_test
    from .sample import sample

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(security_test,url_prefix='/unit')
    app.register_blueprint(sample,url_prefix='/response')

    from .models import User

    create_database(app)
    
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

    
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')