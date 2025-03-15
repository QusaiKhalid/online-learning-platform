from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.extensions import db, migrate
from app.domain.models import User, Course, Lesson, Enrollment, Progress
from app.presentation.controllers.user_controller import register_user_routes
from app.presentation.controllers.keycloak_authurization_controller import register_auth_routes

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration
    from app.config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    # Initialize Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='Online Learning Platform API',
        description='API for managing users and courses',
        doc='/api/docs'
    )

    # Register namespaces (I tried to create restful api for communication between frontend and backend using Flask-RESTX and to compare it with gRPC)
    register_user_routes(api)
    register_auth_routes(api)

    return app