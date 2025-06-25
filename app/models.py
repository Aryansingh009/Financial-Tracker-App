# Import the SQLAlchemy instance from the app package
from app import db

# Import password hashing utilities from Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

# Import datetime for working with dates
from datetime import datetime

# 🧑 User model - represents a registered user in the system
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key: unique ID for each user
    username = db.Column(db.String(25), nullable=False, unique=True)  # Username (must be unique and not null)
    password_hash = db.Column(db.String(50), nullable=False)  # Hashed password for secure storage

    # One-to-many relationship: a user can have multiple transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    # Set password using a secure hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Hash and store the password

    # Verify the provided password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Return True if password matches

# 💸 Transaction model - represents an income or expense entry
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key: unique ID for each transaction
    type = db.Column(db.String(10), nullable=False)  # Type: "income" or "expense"
    category = db.Column(db.String(100), nullable=False)  # Category: e.g., "Food", "Rent", etc.
    amount = db.Column(db.Float, nullable=False)  # Amount of the transaction
    description = db.Column(db.String(255))  # Optional description or notes
    date = db.Column(db.Date, nullable=False)  # Date of the transaction (required)
    
    # Foreign key to associate this transaction with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
