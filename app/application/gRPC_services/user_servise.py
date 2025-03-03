import grpc
from protos.generated import user_pb2, user_pb2_grpc
from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.application import gRPC_helpers as grpc_helpers
import logging
from app.application.security import hash_password
from app.application.auth_decorator import authenticate_grpc_method  # Import the decorator

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    @authenticate_grpc_method
    def GetUserById(self, request, context):
        try:
            user = self.user_repository.get_by_id(request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()
            return grpc_helpers.user_to_proto(user)
        except Exception as e:
            logging.error(f"Error fetching user by ID: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    @authenticate_grpc_method
    def GetUserByEmail(self, request, context):
        try:
            user = self.user_repository.get_by_email(request.email)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()
            return grpc_helpers.user_to_proto(user)
        except Exception as e:
            logging.error(f"Error fetching user by email: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    @authenticate_grpc_method
    def GetUserByUsername(self, request, context):
        try:
            user = self.user_repository.get_by_username(request.username)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()
            return grpc_helpers.user_to_proto(user)
        except Exception as e:
            logging.error(f"Error fetching user by username: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()

    @authenticate_grpc_method
    def GetAllUsers(self, request, context):
        try:
            users = self.user_repository.get_all()
            response = user_pb2.GetAllUsersResponse()
            for user in users:
                response.users.append(grpc_helpers.user_to_proto(user))
            return response
        except Exception as e:
            logging.error(f"Error fetching all users: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetAllUsersResponse()

    @authenticate_grpc_method
    def CreateUser(self, request, context):
        try:
            # Validate email format
            if not self._validate_email(request.email):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid email format")
                return user_pb2.BaseResponse(success=False, message="Invalid email format")

            # Hash password before saving
            hashed_password = hash_password(request.password)

            # Determine the role (use "student" as the default if not provided)
            role = request.role if request.role else "student"

            new_user = User(
                email=request.email,
                username=request.username,
                hashed_password=hashed_password,  # Store the hashed password
                role=role  # Set the role explicitly
            )
            created_user = self.user_repository.create(new_user)
            return grpc_helpers.success_response(f"User {created_user.id} created successfully")
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")

    @authenticate_grpc_method
    def UpdateUser(self, request, context):
        try:
            # Fetch the existing user
            existing_user = self.user_repository.get_by_id(request.id)
            if not existing_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")

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
        except Exception as e:
            logging.error(f"Error updating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")

    @authenticate_grpc_method
    def DeleteUser(self, request, context):
        try:
            # Attempt to soft-delete the user
            deleted = self.user_repository.delete(request.id)
            if not deleted:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")
            return grpc_helpers.success_response(f"User {request.id} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.BaseResponse(success=False, message="Internal server error")

    # Email validation
    def _validate_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None