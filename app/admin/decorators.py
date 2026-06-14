from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from flask import flash, redirect, url_for
from flask_login import current_user
from werkzeug.wrappers import Response

P = ParamSpec("P")
R = TypeVar("R")


def admin_required(view_func: Callable[P, R]) -> Callable[P, R | Response]:
    """Require an authenticated admin user for an admin view."""

    @wraps(view_func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R | Response:
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("main.index"))
        return view_func(*args, **kwargs)

    return cast(Callable[P, R | Response], wrapped)
