from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize extensions.
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name: str | None = None) -> Flask:
    """Application factory."""
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    from config import config

    selected_config = config_name or app.config.get("ENV") or "development"
    app.config.from_object(config[selected_config])
    _validate_production_config(app, selected_config)

    from app.logging import configure_logging

    configure_logging(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    _init_extensions(app)
    _register_blueprints(app)
    _register_login(app)

    from app.api import register_api
    from app.errors import register_error_handlers
    from app.template_filters import register_template_filters

    register_api(app)
    register_error_handlers(app)
    register_template_filters(app)

    return app


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", []) or "*"}},
    )
    migrate.init_app(app, db)
    csrf.init_app(app)


def _register_blueprints(app: Flask) -> None:
    from app.admin import admin_bp
    from app.auth import auth_bp
    from app.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")


def _register_login(app: Flask) -> None:
    @login_manager.user_loader  # type: ignore[misc]
    def load_user(user_id: str) -> object | None:
        from app.models.user import User

        return db.session.get(User, int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"


def _validate_production_config(app: Flask, config_name: str) -> None:
    """Fail fast for missing critical production configuration."""
    if config_name != "production":
        return

    secret_key = app.config.get("SECRET_KEY")
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")

    if not secret_key or secret_key == "dev-secret-key-change-in-production":
        raise RuntimeError("SECRET_KEY must be set to a secure value in production")
    if not db_uri:
        raise RuntimeError("DATABASE_URL must be set in production")
