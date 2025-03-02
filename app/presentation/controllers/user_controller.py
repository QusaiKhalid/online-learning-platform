from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.application.services.user_servise import UserService
# Create a new namespace for user operations
user_ns = Namespace('users', description='User related operations')

# Define the request models
user_model = user_ns.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'email': fields.String(required=True, description='User email'),
    'username': fields.String(required=True, description='Username'),
    # Add other fields as needed
})

# Register the namespace
def register_user_routes(api):
    api.add_namespace(user_ns)

@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """List all users."""
        users = UserService.get_all()
        return users

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user."""
        data = request.json
        new_user = UserService.create(data)
        return new_user, 201

@user_ns.route('/<int:user_id>')
class UserResource(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user by ID."""
        user = UserService.get_by_id(user_id)
        if user:
            return user
        user_ns.abort(404, message=f"User with ID {user_id} not found")

    @user_ns.doc('update_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user by ID."""
        data = request.json
        updated_user = UserService.update(user_id, data)
        if updated_user:
            return updated_user
        user_ns.abort(404, message=f"User with ID {user_id} not found")

    @user_ns.doc('delete_user')
    @user_ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user by ID."""
        UserService.delete(user_id)
        return '', 204

@user_ns.route('/email/<string:email>')
class UserByEmail(Resource):
    @user_ns.doc('get_user_by_email')
    @user_ns.marshal_with(user_model)
    def get(self, email):
        """Fetch a user by email."""
        user = UserService.get_user_by_email(email)
        if user:
            return user
        user_ns.abort(404, message=f"User with email {email} not found")

@user_ns.route('/username/<string:username>')
class UserByUsername(Resource):
    @user_ns.doc('get_user_by_username')
    @user_ns.marshal_with(user_model)
    def get(self, username):
        """Fetch a user by username."""
        user = UserService.get_user_by_username(username)
        if user:
            return user
        user_ns.abort(404, message=f"User with username {username} not found")