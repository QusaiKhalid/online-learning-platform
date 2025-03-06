import grpc
from protos.generated import user_pb2, user_pb2_grpc
from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.application import gRPC_helpers as grpc_helpers
import logging
from app.application.security import hash_password, validate_email, authorize_with_opa, AuthenticationError  # Updated import

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def _handle_authentication_error(self, error: AuthenticationError, context):
        """Helper method to handle AuthenticationError exceptions."""
        context.set_code(error.code)
        context.set_details(error.details)
        return user_pb2.GetUserResponse()  # Return an empty response or appropriate default

    def GetUserById(self, request, context):
        try:
            # Fetch the user from the database using the provided database ID
            user = self.user_repository.get_by_id(request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            # Extract the Keycloak ID from the fetched user
            keycloak_id = user.keycloak_id

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id)

            # Return the user details
            return grpc_helpers.user_to_proto(user)

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error fetching user by ID: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    def GetUserByEmail(self, request, context):
        try:
            # Fetch the user from the database using the provided email
            user = self.user_repository.get_by_email(request.email)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            # Extract the Keycloak ID from the fetched user
            keycloak_id = user.keycloak_id

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id)

            # Return the user details
            return grpc_helpers.user_to_proto(user)

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error fetching user by email: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    def GetUserByUsername(self, request, context):
        try:
            # Fetch the user from the database using the provided username
            user = self.user_repository.get_by_username(request.username)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            # Extract the Keycloak ID from the fetched user
            keycloak_id = user.keycloak_id

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id)

            # Return the user details
            return grpc_helpers.user_to_proto(user)

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error fetching user by username: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    def GetAllUsers(self, request, context):
        try:
            logging.info("GetAllUsers method invoked.")

            # Authenticate and authorize using authorize_with_opa (only admins can fetch all users)
            authorize_with_opa(context, action="read", resource_type="users")
            logging.info("Authentication successful. Fetching all users...")

            users = self.user_repository.get_all()
            response = user_pb2.GetAllUsersResponse()
            for user in users:
                response.users.append(grpc_helpers.user_to_proto(user))
            return response

        except AuthenticationError as e:
            logging.error(f"Authentication failed: {e.details}")
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error fetching all users: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetAllUsersResponse()

    def CreateUser(self, request, context):
        try:
            # Authenticate using authorize_with_opa (only admins can create users)
            authorize_with_opa(context, action="create", resource_type="user")

            # Validate email format
            if not validate_email(request.email):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid email format")
                return user_pb2.BaseResponse(success=False, message="Invalid email format")

            # Hash password before saving
            hashed_password = hash_password(request.password)

            # Determine the role (default to "student" if not provided)
            role = request.role if request.role else "student"

            # Ensure the role is valid
            if role not in ['admin', 'teacher', 'student']:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid role specified")
                return user_pb2.BaseResponse(success=False, message="Invalid role")

            new_user = User(
                email=request.email,
                username=request.username,
                hashed_password=hashed_password,  # Store the hashed password
                role=role  # Set the role explicitly
            )
            created_user = self.user_repository.create(new_user)
            return grpc_helpers.success_response(f"User {created_user.id} created successfully")

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")

    def UpdateUser(self, request, context):
        try:
            # Fetch the existing user
            existing_user = self.user_repository.get_by_id(request.id)
            if not existing_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")

            # Extract the Keycloak ID from the fetched user
            keycloak_id = existing_user.keycloak_id

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="update", resource_type="user", resource_id=keycloak_id)

            # Prepare the data to update
            entity_data = {}
            if request.email:
                entity_data["email"] = request.email
            if request.username:
                entity_data["username"] = request.username

            # Call the repository's update method
            updated_user = self.user_repository.update(request.id, entity_data)
            if not updated_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")

            return grpc_helpers.success_response(f"User {request.id} updated successfully")

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error updating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")

    def DeleteUser(self, request, context):
        try:
            # Fetch the existing user
            existing_user = self.user_repository.get_by_id(request.id)
            if not existing_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")

            # Extract the Keycloak ID from the fetched user
            keycloak_id = existing_user.keycloak_id

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="delete", resource_type="user", resource_id=keycloak_id)

            # Attempt to soft-delete the user
            deleted = self.user_repository.delete(request.id)
            if not deleted:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")
            return grpc_helpers.success_response(f"User {request.id} deleted successfully")

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logging.error(f"Error deleting user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")