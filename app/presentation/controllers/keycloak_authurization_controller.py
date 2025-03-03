from flask import request, jsonify
from flask_restx import Resource  # Import Resource from Flask-RESTX
from app.infrastructure.keycloak_auth import keycloak_openid  # Import Keycloak client

def register_auth_routes(api):
    """
    Register authentication-related routes with the Flask-RESTX API.
    """

    # Define a Resource class for the /auth/login endpoint
    class Login(Resource):
        def post(self):
            try:
                # Extract credentials from the request
                data = request.get_json()
                username = data.get("username")
                password = data.get("password")

                if not username or not password:
                    return {"error": "Username and password are required"}, 400

                # Authenticate with Keycloak
                tokens = keycloak_openid.token(username, password)

                # Return tokens to the client
                return {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "expires_in": tokens["expires_in"]
                }, 200

            except Exception as e:
                return {"error": "Invalid credentials"}, 401

    # Define a Resource class for the /auth/logout endpoint
    class Logout(Resource):
        def post(self):
            try:
                # Extract refresh token from the request
                data = request.get_json()
                refresh_token = data.get("refresh_token")

                if not refresh_token:
                    return {"error": "Refresh token is required"}, 400

                # Revoke the token
                keycloak_openid.logout(refresh_token)

                return {"message": "Logged out successfully"}, 200

            except Exception as e:
                return {"error": "Logout failed"}, 500

    # Define a Resource class for the /auth/refresh-token endpoint
    class RefreshToken(Resource):
        def post(self):
            try:
                # Extract refresh token from the request
                data = request.get_json()
                refresh_token = data.get("refresh_token")

                if not refresh_token:
                    return {"error": "Refresh token is required"}, 400

                # Fetch new tokens
                tokens = keycloak_openid.refresh_token(refresh_token)

                return {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "expires_in": tokens["expires_in"]
                }, 200

            except Exception as e:
                return {"error": "Token refresh failed"}, 401

    # Register the resources with the API
    api.add_resource(Login, "/auth/login")
    api.add_resource(Logout, "/auth/logout")
    api.add_resource(RefreshToken, "/auth/refresh-token")