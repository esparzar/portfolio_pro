from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, CSRFError
import logging
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Initialize Flask-RESTful API
    api = Api(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register API resources
    from app.api.resources.contact import ContactResource, ContactDetailResource, ContactStatsResource
    from app.api.resources.projects import ProjectsResource, ProjectDetailResource
    from app.api.resources.auth import AuthResource
    
    api.add_resource(ContactResource, '/api/contacts', '/api/contacts/')
    api.add_resource(ContactDetailResource, '/api/contacts/<int:contact_id>')
    api.add_resource(ContactStatsResource, '/api/contacts/stats')
    api.add_resource(ProjectsResource, '/api/projects', '/api/projects/')
    api.add_resource(ProjectDetailResource, '/api/projects/<int:project_id>')
    api.add_resource(AuthResource, '/api/auth', '/api/auth/')
    
    # ============================================
    # ERROR HANDLERS
    # ============================================
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(429)
    def too_many_requests_error(error):
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/404.html'), 400
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template('errors/csrf.html'), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/404.html'), 401
    
    # ============================================
    # AUTO CREATE ADMIN USER
    # ============================================
    
    with app.app_context():
        db.create_all()
        
        from app.models.user import User
        import os
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Try to get admin password from environment variable
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            
            admin = User(
                username=admin_username,
                email=admin_email,
                is_admin=True,
                is_active=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            app.logger.info(f'Auto-created admin user: {admin_username}')
            print(f'✅ Auto-created admin user: {admin_username}')
        else:
            print(f'✓ Admin user already exists: {admin.username}')
    
    # ============================================
    # USER LOADER FOR FLASK-LOGIN
    # ============================================
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # ============================================
    # CONTEXT PROCESSORS
    # ============================================
    
    @app.context_processor
    def inject_year():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}
    
    return app