import logging
import grpc
from keycloak import KeycloakError
from app.application.security import hash_password
from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from protos.generated.auth_pb2 import LoginResponse, LogoutResponse, RefreshTokenResponse, SignUpResponse
from protos.generated.auth_pb2_grpc import AuthServiceServicer
from app.infrastructure.keycloak_auth import assign_role_to_user, keycloak_openid, keycloak_admin

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class AuthServicer(AuthServiceServicer):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def SignUp(self, request, context):
        try:
            # Extract user details from the request
            username = request.username
            email = request.email
            password = request.password
            first_name = request.first_name
            last_name = request.last_name
            role = request.role  # New field for role

            if not all([username, email, password, role]):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Username, email, password, and role are required")
                return SignUpResponse()

            # Create the user in Keycloak
            user_data = {
                "username": username,
                "email": email,
                "enabled": True,
                "firstName": first_name,
                "lastName": last_name,
                "credentials": [
                    {
                        "type": "password",
                        "value": password,
                        "temporary": False,
                    }
                ],
            }
            keycloak_user_id = keycloak_admin.create_user(user_data)

            # Assign a role to the user in Keycloak
            assign_role_to_user(keycloak_user_id, role)

            # Hash the password before storing it in the local database
            hashed_password = hash_password(password)

            # Add the user to the local database
            local_user = User(
                keycloak_id=keycloak_user_id,
                username=username,
                email=email,
                hashed_password=hashed_password,
                role=role,
                is_deleted=False,
            )
            self.user_repository.create(local_user)

            return SignUpResponse(message=f"User {username} created successfully")
        except KeycloakError as e:
            logging.error(f"SignUp failed (Keycloak): {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to create user in Keycloak: {str(e)}")
            return SignUpResponse()
        except Exception as e:
            logging.error(f"SignUp failed (Database): {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to create user in the local database: {str(e)}")
            return SignUpResponse()

    def Login(self, request, context):
        try:
            # Extract credentials from the request
            username = request.username
            password = request.password

            if not username or not password:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Username and password are required")
                return LoginResponse()

            # Authenticate with Keycloak
            tokens = keycloak_openid.token(username, password)

            # Validate the access token
            token_info = keycloak_openid.introspect(tokens["access_token"])
            if not token_info["active"]:
                raise Exception("Invalid token")

            # Return tokens to the client
            return LoginResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_in=tokens["expires_in"],
                user_id=token_info["sub"],  # Include user ID from token
                role=token_info.get("role", "user")  # Include role from token
            )
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return LoginResponse()

    def Logout(self, request, context):
        try:
            # Extract tokens from the request
            refresh_token = request.refresh_token
            access_token = request.access_token  # Add this field to the proto

            if not refresh_token or not access_token:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Refresh token and access token are required")
                return LogoutResponse()

            # Revoke the tokens
            keycloak_openid.logout(refresh_token)
            keycloak_openid.revoke_token(access_token)

            return LogoutResponse(message="Logged out successfully")
        except Exception as e:
            logging.error(f"Logout failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Logout failed")
            return LogoutResponse()

    def RefreshToken(self, request, context):
        try:
            # Extract refresh token from the request
            refresh_token = request.refresh_token

            if not refresh_token:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Refresh token is required")
                return RefreshTokenResponse()

            # Fetch new tokens
            tokens = keycloak_openid.refresh_token(refresh_token)

            # Validate the new access token
            token_info = keycloak_openid.introspect(tokens["access_token"])
            if not token_info["active"]:
                raise Exception("Invalid token")

            return RefreshTokenResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_in=tokens["expires_in"]
            )
        except Exception as e:
            logging.error(f"Token refresh failed: {str(e)}")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Token refresh failed")
            return RefreshTokenResponse()