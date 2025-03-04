import requests
import grpc
from app.infrastructure.keycloak_auth import keycloak_openid
import bcrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64

# Configure password hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class AuthenticationError(Exception):
    def __init__(self, code, details):
        self.code = code
        self.details = details

def get_keycloak_public_key():
    try:
        openid_config_url = "http://localhost:8080/realms/online-learning-platform/.well-known/openid-configuration"
        openid_config_response = requests.get(openid_config_url)
        openid_config_response.raise_for_status()
        openid_config = openid_config_response.json()

        jwks_uri = openid_config["jwks_uri"]
        jwks_response = requests.get(jwks_uri)
        jwks_response.raise_for_status()
        jwks = jwks_response.json()

        key_data = jwks["keys"][0]  # Get the first key (assuming only one key exists)

        # Decode the JWK RSA public key
        public_key = rsa.RSAPublicNumbers(
            e=int.from_bytes(base64.urlsafe_b64decode(key_data["e"] + "==="), "big"),
            n=int.from_bytes(base64.urlsafe_b64decode(key_data["n"] + "==="), "big"),
        ).public_key(default_backend())

        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

    except Exception:
        raise AuthenticationError(grpc.StatusCode.INTERNAL, "Failed to fetch Keycloak public key")

def authenticate(context, required_roles=None):
    metadata = dict(context.invocation_metadata())
    auth_header = metadata.get('authorization', '')

    if not auth_header.startswith('Bearer '):
        raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, 'Authorization header missing or invalid')

    token = auth_header.split('Bearer ')[1]

    try:
        public_key = get_keycloak_public_key()
        token_info = keycloak_openid.decode_token(token, validate=True)
        user_roles = token_info.get('realm_access', {}).get('roles', [])

    except Exception:
        raise AuthenticationError(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')

    if required_roles and not any(role in user_roles for role in required_roles):
        raise AuthenticationError(grpc.StatusCode.PERMISSION_DENIED, 'Insufficient permissions')

    return token_info
