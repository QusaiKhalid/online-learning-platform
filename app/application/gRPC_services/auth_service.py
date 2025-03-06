import logging
from concurrent import futures
import grpc
from protos.generated.auth_pb2 import LoginResponse, LogoutResponse, RefreshTokenResponse
from protos.generated.auth_pb2_grpc import AuthServiceServicer
from app.infrastructure.keycloak_auth import keycloak_openid  # Import Keycloak client

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class AuthServicer(AuthServiceServicer):
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

            # Return tokens to the client
            return LoginResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_in=tokens["expires_in"]
            )
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return LoginResponse()

    def Logout(self, request, context):
        try:
            # Extract refresh token from the request
            refresh_token = request.refresh_token

            if not refresh_token:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Refresh token is required")
                return LogoutResponse()

            # Revoke the token
            keycloak_openid.logout(refresh_token)

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