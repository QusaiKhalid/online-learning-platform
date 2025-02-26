import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # Debug mode (set to False in production)
    DEBUG = True

    # Secret key for session management and security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Database connection string
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')

    # Disable SQLAlchemy event system to reduce overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keycloak server URL
    KEYCLOAK_SERVER = os.getenv('KEYCLOAK_SERVER', 'http://localhost:8080/auth')

    # Keycloak realm name
    KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM', 'online-learning-platform')

    # Keycloak client ID
    KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', 'flask-backend')

    # Keycloak client secret
    KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET', 'default_keycloak_secret')
