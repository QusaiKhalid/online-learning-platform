from keycloak import KeycloakOpenID
from app.config import Config

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_CLIENT_SECRET
)