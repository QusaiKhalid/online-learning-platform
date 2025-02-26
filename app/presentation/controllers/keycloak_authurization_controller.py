from flask import Blueprint, request, jsonify, current_app
from flask_restx import Namespace, Resource, fields

# Create a new namespace for authentication
auth_ns = Namespace('auth', description='Authentication related operations')

# Define the request model for login
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

# Register the namespace
def register_routes(api):
    api.add_namespace(auth_ns)

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Log in a user and return a token."""
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Access Keycloak client from the current app context
        keycloak_openid = current_app.keycloak_openid

        try:
            # Use Keycloak to obtain the token
            token = keycloak_openid.token(username, password)
            return jsonify(token)
        except Exception as e:
            return {'message': str(e)}, 401
        
@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        """Log out the user."""
        # Get the token from the request (e.g., from headers or body)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is missing'}, 400

        # Check if the header is in the correct format (Bearer <token>)
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return {'message': 'Invalid Authorization header format'}, 400

        token = parts[1]

        # Access Keycloak client from the current app context
        keycloak_openid = current_app.keycloak_openid

        try:
            # Use Keycloak to revoke the token
            keycloak_openid.logout(token)
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'message': str(e)}, 400
