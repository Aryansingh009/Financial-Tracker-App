# Import necessary modules
from flask import Flask, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  # For ORM/database handling
from flask_wtf import CSRFProtect        # For securing forms against CSRF attacks
import uuid                              # To generate unique IDs (used for session validation)

# Initialize SQLAlchemy and CSRF globally (but not bound to app yet)
db = SQLAlchemy()
csrf = CSRFProtect()

# Factory function to create and configure the Flask app
def create_app():
    app = Flask(__name__)  # Create the Flask app instance

    # App configuration
    app.config['SECRET_KEY'] = "my-secret-key"  # Secret key used for session encryption, CSRF protection, etc.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'  # Database URI (using SQLite file named tracker.db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications (saves memory and performance)

    # Initialize database extension with the app
    db.init_app(app)

    # Import and register route blueprints (modular parts of the app)
    from app.routes.auth import auth_bp              # Authentication-related routes
    from app.routes.transaction import transaction_bp  # Routes related to transactions
    # from app.routes.forms import forms_bp           # (Commented out) Possible routes for forms
    from app.routes.init import init_bp              # Initialization/setup-related routes

    app.register_blueprint(auth_bp)                  # Register auth routes with app
    app.register_blueprint(transaction_bp)           # Register transaction routes with app
    # app.register_blueprint(forms_bp)               # Commented out: skip forms_bp
    app.register_blueprint(init_bp)                  # Register init routes with app

    # Initialize CSRF protection with app
    csrf.init_app(app)

    # 🔐 Generate a unique boot ID every time the server restarts
    server_boot_id = str(uuid.uuid4())               # Generate a new UUID for server instance
    app.config['SERVER_BOOT_ID'] = server_boot_id    # Store it in app config

    # 🚦 Middleware: runs before every request
    @app.before_request
    def check_session_expired():
        # If the user is logged in (user_id in session)
        if 'user_id' in session:
            # Check if session boot ID matches current server boot ID
            if session.get('boot_id') != app.config['SERVER_BOOT_ID']:
                session.clear()  # Clear the session (force logout)
                flash("Session expired. Please log in again.", "warning")  # Show message
                return redirect(url_for('auth.login'))  # Redirect to login page

    return app  # Return the configured app instance
