from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
db_name = 'database.sqlite' 


def create_database():
    db.create_all()
    print('Database Created')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'afdslkjadfk dfgsgf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import customer, cart, product, order

    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/') 
    app.register_blueprint(admin, url_prefix='/')

    with app.app_context():
        create_database()

    return app