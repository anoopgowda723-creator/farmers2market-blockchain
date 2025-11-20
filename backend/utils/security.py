# backend/utils/security.py
from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If not logged in via Flask-Login, send to login page
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))

        # (Optional) keep your old session-based check if you still rely on it
        if "user_id" not in session:
            session["user_id"] = current_user.id

        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    """
    Ensure the current user has one of the allowed roles.
    Usage: @role_required("FARMER", "ADMIN")
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login"))

            if current_user.role not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("main.home"))

            return f(*args, **kwargs)

        return decorated_function

    return wrapper
