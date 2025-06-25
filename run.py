# Import the application factory function from your app package
from app import create_app

# Create the Flask app instance by calling the factory
app = create_app()

# If this file is run directly (not imported as a module), start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode (useful during development)
