from typing import Any, Self, cast

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.utils.datetime import utc_now


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    last_login = db.Column(db.DateTime)

    # projects = db.relationship('Project', back_populates='user', foreign_keys='Project.user_id')

    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str) -> Self | None:
        """Authenticate user"""
        user = cast(Self | None, cls.query.filter_by(username=username, is_active=True).first())
        if user and user.check_password(password):
            user.last_login = utc_now()
            db.session.commit()
            return user
        return None

    def get_id(self) -> str:
        """Return user ID for Flask-Login"""
        return str(self.id)

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
