from flask_jwt_extended import get_jwt_identity

from app import db
from app.models.user import User


def get_current_user():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return None
    return db.session.get(User, user_id)


def get_current_admin():
    user = get_current_user()
    if not user or not user.is_admin:
        return None
    return user
