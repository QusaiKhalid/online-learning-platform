from flask import jsonify

def register_routes(app):
    """
    Register all API routes with the Flask app.
    """
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Online Learning Platform API!"})