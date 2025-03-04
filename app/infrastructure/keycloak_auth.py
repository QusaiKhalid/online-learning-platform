from keycloak import KeycloakOpenID
from app.config import Config

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_CLIENT_SECRET
)

def decode_and_validate_token(token):
    """
    Decode and validate a Keycloak token.
    """
    try:
        token_info = keycloak_openid.decode_token(
            token,
            options={"verify_signature": True, "verify_aud": True, "verify_exp": True}
        )
        return token_info
    except Exception as e:
        raise ValueError("Invalid token")