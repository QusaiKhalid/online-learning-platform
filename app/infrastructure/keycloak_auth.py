import sys
import os

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from keycloak import KeycloakOpenID, KeycloakAdmin
from app.config import Config
from keycloak.exceptions import KeycloakError
import logging

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_CLIENT_SECRET
)

# Initialize Keycloak admin client
keycloak_admin = KeycloakAdmin(
    server_url="http://localhost:8080",
    username="hello",
    password="123",
    realm_name="online-learning-platform",
    client_id="api-flask",
    client_secret_key="Okb6fbRp1JHooQp89Zk60exEUSPXUaNg",
    verify=True
)

def assign_role_to_user(keycloak_user_id: str, role: str):
    """
    Assign a role to a user in Keycloak.
    """
    try:
        # Fetch the role from Keycloak
        role_representation = keycloak_admin.get_realm_role(role)
        if not role_representation:
            raise Exception(f"Role '{role}' not found in Keycloak")

        # Assign the role to the user
        keycloak_admin.assign_realm_roles(keycloak_user_id, [role_representation])
    except KeycloakError as e:
        logging.error(f"Failed to assign role to user: {str(e)}")
        raise