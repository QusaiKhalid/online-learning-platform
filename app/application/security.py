import logging
import requests
import grpc
from app.infrastructure.keycloak_auth import keycloak_openid
import bcrypt
import json
import base64
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Email validation
def validate_email(self, email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    logger.info(f"Validating email: {email}")
    return re.match(pattern, email) is not None

# Configure password hashing
def hash_password(password: str) -> str:
    logger.info("Hashing password")
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class AuthenticationError(Exception):
    def __init__(self, code, details):
        self.code = code
        self.details = details

def validate_token(token: str):
    """
    Validate the JWT token (expiration, issuer, audience, and signature).
    """
    try:
        logger.info("Validating token")
        # Decode the token header to get the key ID (kid)
        header = token.split(".")[0]
        header_data = base64.urlsafe_b64decode(header + "===").decode("utf-8")
        header_dict = json.loads(header_data)  # Convert string to dictionary
        token_kid = header_dict.get("kid")

        if not token_kid:
            logger.error("Token header missing key ID (kid)")
            raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, "Token header missing key ID (kid)")

        # Decode and validate the token
        token_info = keycloak_openid.decode_token(token)

        logger.info("Token decoded successfully")
        # Validate token claims
        now = datetime.now(timezone.utc).timestamp()
        if token_info.get("exp", 0) < now:
            logger.error("Token has expired")
            raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, "Token has expired")

        if token_info.get("iss") != "http://localhost:8080/realms/online-learning-platform":
            logger.error("Invalid token issuer")
            raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, "Invalid token issuer")

        # if "your-audience" not in token_info.get("aud", []):  # Replace with your actual audience
        #     logger.error("Invalid token audience")
        #     raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, "Invalid token audience")

        logger.info("Token validation successful")
        return token_info

    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
    
def authenticate(context, required_roles=None):
    """
    Authenticate the user and validate their roles.
    """
    try:
        logger.info("Authenticating user")
        metadata = dict(context.invocation_metadata())
        auth_header = metadata.get('authorization', '')

        if not auth_header.startswith('Bearer '):
            logger.error("Authorization header missing or invalid")
            raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, 'Authorization header missing or invalid')

        token = auth_header.split('Bearer ')[1]

        token_info = validate_token(token)
        user_roles = token_info.get('realm_access', {}).get('roles', [])

        logger.info(f"User roles: {user_roles}")
        if required_roles and not any(role in user_roles for role in required_roles):
            logger.error("Insufficient permissions")
            raise AuthenticationError(grpc.StatusCode.PERMISSION_DENIED, 'Insufficient permissions')

        logger.info(f"User {token_info.get('preferred_username')} authenticated successfully")
        return token_info

    except AuthenticationError as e:
        logger.error(f"Authentication error: {e.details}")
        raise e
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, 'Authentication failed')

def authorize_with_opa(context, action, resource_type, resource_id=None):
    """
    Perform OPA authorization for the given action and resource.
    """
    try:
        logger.info(f"Action: {action}, Resource type: {resource_type}, Resource ID: {resource_id}")

        logger.info("Authorizing with OPA")
        # Authenticate the user and retrieve their roles
        token_info = authenticate(context)
        user_roles = token_info.get('realm_access', {}).get('roles', [])
        user_info = {
            "id": token_info.get("sub"),
            "username": token_info.get("preferred_username"),
            "roles": user_roles
        }
        logger.info(f"User info: {user_info}")
        # Validate resource ID to prevent injection attacks
        if resource_id and not isinstance(resource_id, str):
            logger.error("Invalid resource ID")
            raise AuthenticationError(grpc.StatusCode.INVALID_ARGUMENT, "Invalid resource ID")
        # Call OPA for authorization
        opa_url = "http://localhost:8181/v1/data/authz/allow"
        input_data = {
            "input": {
                "user": user_info,
                "action": action,
                "resource": {
                    "type": resource_type,
                    "id": resource_id   # Default to user's ID if not specified
                }
            }
        }

        logger.info(f"Sending request to OPA: {input_data}")
        response = requests.post(opa_url, json=input_data)
        if response.status_code != 200:
            logger.error(f"OPA authorization failed: {response.text}")
            raise AuthenticationError(grpc.StatusCode.INTERNAL, "OPA authorization failed")

        result = response.json()
        if not result.get("result", False):
            logger.error("Access denied by OPA")
            raise AuthenticationError(grpc.StatusCode.PERMISSION_DENIED, 'Access denied by OPA')

        logger.info(f"User {user_info['username']} authorized for {action} on {resource_type}/{resource_id}")
        return True

    except AuthenticationError as e:
        logger.error(f"Authorization error: {e.details}")
        raise e
    except Exception as e:
        logger.error(f"Error during OPA authorization: {str(e)}")
        raise AuthenticationError(grpc.StatusCode.INTERNAL, "Internal server error during OPA authorization")