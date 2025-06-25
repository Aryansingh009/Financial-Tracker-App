# Import the Flask app factory and the database instance
from app import create_app, db

# Create an instance of the app using the factory function
app = create_app()

# Enter the application context to safely work with Flask-specific features like the database
with app.app_context():
    db.create_all()  # Create all database tables defined in your models (User, Transaction, etc.)
    print("Database tables created.")  # Confirmation message
