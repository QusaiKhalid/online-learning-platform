from flask import request, jsonify
from app.infrastructure.keycloak_auth import keycloak_openid  # Import Keycloak client

def register_auth_routes(api):
    """
    Register authentication-related routes with the Flask-RESTX API.
    """
    @api.route("/auth/login", methods=["POST"])
    def login():
        try:
            # Extract credentials from the request
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400

            # Authenticate with Keycloak
            tokens = keycloak_openid.token(username, password)

            # Return tokens to the client
            return jsonify({
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "expires_in": tokens["expires_in"]
            }), 200

        except Exception as e:
            return jsonify({"error": "Invalid credentials"}), 401

    @api.route("/auth/logout", methods=["POST"])
    def logout():
        try:
            # Extract refresh token from the request
            data = request.get_json()
            refresh_token = data.get("refresh_token")

            if not refresh_token:
                return jsonify({"error": "Refresh token is required"}), 400

            # Revoke the token
            keycloak_openid.logout(refresh_token)

            return jsonify({"message": "Logged out successfully"}), 200

        except Exception as e:
            return jsonify({"error": "Logout failed"}), 500

    @api.route("/auth/refresh-token", methods=["POST"])
    def refresh_token():
        try:
            # Extract refresh token from the request
            data = request.get_json()
            refresh_token = data.get("refresh_token")

            if not refresh_token:
                return jsonify({"error": "Refresh token is required"}), 400

            # Fetch new tokens
            tokens = keycloak_openid.refresh_token(refresh_token)

            return jsonify({
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "expires_in": tokens["expires_in"]
            }), 200

        except Exception as e:
            return jsonify({"error": "Token refresh failed"}), 401