from venv import logger
import grpc
from protos.generated import user_pb2, user_pb2_grpc
from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.application import gRPC_helpers as grpc_helpers
import logging
from app.application.security import hash_password, validate_email, authorize_with_opa, authenticate, get_organization_id, AuthenticationError
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            logger.info(f"Fetching user with ID {request.id} for organization {organization_id}")
            
            # Fetch the user from the database using the provided database ID and organization ID
            user = self.user_repository.get_by_id(request.id, organization_id)

            if not user:
                logger.warning(f"User with ID {request.id} not found in organization {organization_id}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            logger.info(f"User found: {user}")

            # Extract the Keycloak ID and organization ID from the fetched user
            keycloak_id = user.keycloak_id
            resourse_organization_id = user.keycloak_organization_id

            if not keycloak_id:
                logger.error(f"User with database ID {request.id} has no associated Keycloak ID")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User has no associated Keycloak ID")
                return user_pb2.GetUserResponse()

            logger.info(f"Authorizing user {keycloak_id} for action 'read' on resource 'user'")

            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id, resource_organization_id=resourse_organization_id)

            logger.info(f"Authorization successful for user {keycloak_id}")

            # Return the user details
            return grpc_helpers.user_to_proto(user)

        except AuthenticationError as e:
            return self._handle_authentication_error(e, context)
        except Exception as e:
            logger.error(f"Error fetching user by ID {request.id}: {str(e)}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return user_pb2.GetUserResponse()


    def GetUserByEmail(self, request, context):
        try:
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            # Fetch the user from the database using the provided email and organization ID
            user = self.user_repository.get_by_email(request.email, organization_id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()
            
            # Extract the Keycloak ID and organization ID from the fetched user
            keycloak_id = user.keycloak_id
            resourse_organization_id = user.keycloak_organization_id
            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id, resource_organization_id=resourse_organization_id)
            
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            # Fetch the user from the database using the provided username and organization ID
            user = self.user_repository.get_by_username(request.username, organization_id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()
            
            # Extract the Keycloak ID and organization ID from the fetched user
            keycloak_id = user.keycloak_id
            resourse_organization_id = user.keycloak_organization_id
            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id, resource_organization_id=resourse_organization_id)
            
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            authorize_with_opa(context, action="read", resource_type="users")
            logging.info("Authentication successful. Fetching all users...")
            
            # Fetch all users for the specified organization
            users = self.user_repository.get_all(organization_id)
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
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
                role=role,  # Set the role explicitly
                organization_id=organization_id  # Associate the user with the organization
            )
            created_user = self.user_repository.create(new_user, organization_id)
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            # Fetch the existing user
            existing_user = self.user_repository.get_by_id(request.id, organization_id)
            if not existing_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")
            
            # Extract the Keycloak ID and organization ID from the fetched user
            keycloak_id = existing_user.keycloak_id
            resourse_organization_id = existing_user.organization_id
            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id, resource_organization_id=resourse_organization_id)
            
            
            # Prepare the data to update
            entity_data = {}
            if request.email:
                entity_data["email"] = request.email
            if request.username:
                entity_data["username"] = request.username
            
            # Call the repository's update method
            updated_user = self.user_repository.update(request.id, entity_data, organization_id)
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
            token_info = authenticate(context)  # Authenticate the request to get the token info
            organization_id = get_organization_id(token_info)  # Extract the organization ID from the token
            
            # Fetch the existing user
            existing_user = self.user_repository.get_by_id(request.id, organization_id)
            if not existing_user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.BaseResponse(success=False, message="User not found")
            
            # Extract the Keycloak ID and organization ID from the fetched user
            keycloak_id = existing_user.keycloak_id
            resourse_organization_id = existing_user.organization_id
            # Authorize using the Keycloak ID as the resource ID
            authorize_with_opa(context, action="read", resource_type="user", resource_id=keycloak_id, resource_organization_id=resourse_organization_id)
            
            
            # Attempt to soft-delete the user
            deleted = self.user_repository.delete(request.id, organization_id)
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