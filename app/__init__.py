from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Load environment variables from .env file
    load_dotenv()

    # Load configurations from the environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Check if the necessary environment variables are loaded
    if not app.config['SECRET_KEY']:
        raise ValueError("SECRET_KEY not set in .env file")
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("SQLALCHEMY_DATABASE_URI not set in .env file")

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from .views import auth, main, products, account, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(admin.bp)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    return app

