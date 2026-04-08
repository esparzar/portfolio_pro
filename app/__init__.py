from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
import os
import logging



# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    
    # Optional: Add CSRF protection (can add later if needed)
    try:
        from flask_wtf.csrf import CSRFProtect
        csrf = CSRFProtect()
        csrf.init_app(app)
    except ImportError:
        pass
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp 

    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)
    
    # Register API blueprint if it exists
    try:
        from app.routes.api import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
    except ImportError:
        pass
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/portfolio.log')
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)
    
    return app
# Auto-create admin user if environment variables are set
def create_admin_if_not_exists():
    """Auto-create admin user from environment variables"""
    from app.models.user import User
    
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD')
    
    if password:
        admin = User.query.filter_by(username=username).first()
        if not admin:
            admin = User(username=username, email=email, is_admin=True, is_active=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f'✅ Auto-created admin user: {username}')
        else:
            print(f'✓ Admin user already exists: {username}')
    else:
        print('⚠️  ADMIN_PASSWORD not set, skipping admin creation')

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))