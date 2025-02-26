from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.extensions import db, migrate
from app.domain.models import User, Course, Lesson, Enrollment, Progress
from keycloak import KeycloakOpenID  # Import KeycloakOpenID

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    # Import models inside the create_app function to prevent circular import.
    app = Flask(__name__)

    # Load configuration
    from app.config import Config  # Import the Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    # Initialize Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='Online Learning Platform API',
        description='API for managing users and courses',
        doc='/api/docs'  # URL for Swagger UI
    )

    # Initialize Keycloak client
    keycloak_openid = KeycloakOpenID(
        server_url=app.config['KEYCLOAK_SERVER'],
        client_id=app.config['KEYCLOAK_CLIENT_ID'],
        realm_name=app.config['KEYCLOAK_REALM'],
        # client_secret_key=app.config['KEYCLOAK_CLIENT_SECRET']
    )

    # Optionally, you can add the Keycloak client to app context
    app.keycloak_openid = keycloak_openid

    # Register namespaces (we'll define these next)
    from app.presentation.controllers.keycloak_authurization_controller import register_routes
    register_routes(api)

    return app
