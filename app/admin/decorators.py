from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(view_func):
    """Require an authenticated admin user for an admin view."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("main.index"))
        return view_func(*args, **kwargs)

    return wrapped
