import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in {"1", "true", "yes", "on"}


class Config:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "app/static/uploads"))
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    RATELIMIT_ENABLED = _env_bool("RATELIMIT_ENABLED", True)
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL", "memory://")
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True

    CORS_ORIGINS = [
        origin.strip() for origin in os.environ.get("CORS_ORIGINS", "").split(",") if origin.strip()
    ]

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY


class LocalConfig(Config):
    """Local workstation configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///portfolio.db"


class DevelopmentConfig(LocalConfig):
    """Shared development/staging configuration."""


class ProductionConfig(Config):
    """Production configuration for Render."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Strict"
    PREFERRED_URL_SCHEME = "https"


class TestingConfig(Config):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


config = {
    "local": LocalConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": LocalConfig,
}
