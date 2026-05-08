from flask import Flask, render_template, url_for
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
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
csrf = CSRFProtect()

# DB/admin may use friendly names; files on disk use screenshot filenames.
PROJECT_IMAGE_ALIASES = {
    'portfolio-home.png': 'homepage-hero.png',
    'portfolio-admin-dashboard.png': 'admin-dashboard.png',
    'portfolio-about.png': 'projects-section.png',
}


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    _validate_production_config(app, config_name)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', []) or "*"}}
    )
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
    from app.api.resources.projects import ProjectListResource, ProjectDetailResource
    from app.api.resources.auth import AuthResource, RegisterResource

    api.add_resource(ContactResource, '/api/contacts', '/api/contacts/')
    api.add_resource(ContactDetailResource, '/api/contacts/<int:contact_id>')
    api.add_resource(ContactStatsResource, '/api/contacts/stats')
    api.add_resource(ProjectListResource, '/api/projects', '/api/projects/')
    api.add_resource(ProjectDetailResource, '/api/projects/<int:project_id>')
    api.add_resource(AuthResource, '/api/auth', '/api/auth/')
    api.add_resource(RegisterResource, '/api/auth/register', '/api/auth/register/')
    
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
    # USER LOADER FOR FLASK-LOGIN
    # ============================================
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))
    
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
    
    import json

    @app.template_filter('from_json')
    def from_json_filter(value):
        """Convert JSON string to Python object"""
        if not value:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, return as is or split by comma
            if isinstance(value, str) and ',' in value:
                return [v.strip() for v in value.split(',')]
            return [value] if value else []

    @app.template_filter('static_image')
    def static_image_filter(path):
        """Resolve a static image path or external URL for use in img src."""
        from flask import current_app

        if path is None:
            return ''
        path = str(path).strip()
        if not path:
            return ''
        lower = path.lower()
        if lower.startswith('http://') or lower.startswith('https://'):
            return path
        path = path.lstrip('/')
        # Truncated extension from some clients (e.g. .pn)
        if lower.endswith('.pn') and not lower.endswith('.png'):
            path = path[:-3] + '.png'
        static_root = os.path.join(current_app.root_path, 'static')

        initial = []
        if path.startswith('images/'):
            initial.append(path)
        else:
            initial.append(f'images/{path}')
            if '/' not in path:
                initial.append(f'images/project/{path}')

        ordered = []
        seen = set()

        def add_candidate(rel_path):
            if rel_path and rel_path not in seen:
                seen.add(rel_path)
                ordered.append(rel_path)

        for rel in initial:
            add_candidate(rel)
            basename = os.path.basename(rel)
            mapped = PROJECT_IMAGE_ALIASES.get(basename.lower())
            if mapped:
                add_candidate(f'images/project/{mapped}')

        for filename in ordered:
            full_path = os.path.join(static_root, filename)
            if os.path.isfile(full_path):
                return url_for('static', filename=filename)

        return url_for('static', filename=ordered[0])

    return app


def _validate_production_config(app, config_name):
    """Fail fast for missing critical production configuration."""
    if config_name != 'production':
        return

    secret_key = app.config.get('SECRET_KEY')
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')

    if not secret_key or secret_key == 'dev-secret-key-change-in-production':
        raise RuntimeError('SECRET_KEY must be set to a secure value in production')
    if not db_uri:
        raise RuntimeError('DATABASE_URL must be set in production')