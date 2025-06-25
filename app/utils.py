# Import wraps to preserve original function's metadata when decorating
from functools import wraps

# Import Flask utilities for session handling and redirection
from flask import session, redirect, url_for, flash

# Custom decorator to protect routes that require login
def login_required(view_func):
    @wraps(view_func)  # Ensures original function name and docstring are preserved
    def wrapper(*args, **kwargs):
        # Check if 'user_id' exists in session (i.e., user is logged in)
        if 'user_id' not in session:
            flash("Login required.")  # Flash message to alert the user
            return redirect(url_for('auth.login'))  # Redirect to login page
        return view_func(*args, **kwargs)  # Proceed to the original view if logged in
    return wrapper  # Return the wrapped function
