# 🔌 Flask imports for handling sessions, templates, redirects, flashing messages, and app context
from flask import Blueprint, render_template, redirect, url_for, session, flash, current_app

# 🔧 Import database and models
from app import db
from app.models import User

# 🧾 Import registration and login forms
from app.routes.forms import RegistrationForm, LoginForm

# 🧩 Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()  # Instantiate the registration form

    if form.validate_on_submit():  # If the form is submitted and valid
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("User already exists", "danger")  # Show error if username is taken
            return redirect(url_for('auth.register'))  # Reload registration page

        # Create a new user with hashed password
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)  # Hash and store password
        db.session.add(new_user)
        db.session.commit()  # Save the user to the database

        flash("Registration successful", "success")  # Show success message
        return redirect(url_for("auth.login"))  # Redirect to login page

    return render_template('register.html', form=form)  # Show form if GET or invalid
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instantiate the login form

    if form.validate_on_submit():  # If form is submitted and valid
        user = User.query.filter_by(username=form.username.data).first()

        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Save user session
            session['user_id'] = user.id
            session['boot_id'] = current_app.config['SERVER_BOOT_ID']  # Store boot ID for session validity
            flash("Logged in successfully", "success")
            return redirect(url_for('transaction_bp.dashboard'))  # Redirect to dashboard
        else:
            flash("Invalid username or password", "danger")  # Show error

    return render_template('login.html', form=form)  # Show login form
@auth_bp.route("/logout")
def logout():
    session.pop('user_id', None)     # Remove user ID from session
    session.pop('boot_id', None)     # Remove server boot ID (used for session validation)
    flash("You have been logged out", "info")  # Show logout message
    return redirect(url_for('auth.login'))  # Redirect to login page
