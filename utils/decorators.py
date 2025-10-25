# eventhive/utils/decorators.py

from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorator that ensures a user has *any* of the specified roles.
    :param roles: A list of required role names (e.g., 'Admin', 'Organizer')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            # Check if the user's role is in the list of allowed roles
            if current_user.role not in roles:
                flash(f"Access denied. You need to be an {', '.join(roles)} to view this page.", "danger")
                return redirect(url_for('events.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator