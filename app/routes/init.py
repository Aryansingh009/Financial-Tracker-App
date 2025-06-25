from flask import Blueprint, redirect, url_for

init_bp = Blueprint('init_bp', __name__)

@init_bp.route('/')
def home():
    return redirect(url_for('auth.login'))  # or render_template('home.html')
