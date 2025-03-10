from sqlalchemy import create_engine, inspect
import os

# Create an engine (connect to your SQLite database)
# You can replace the database URL with your environment variable or path to the database
DATABASE_URL = 'sqlite:///instance/app.db'
  # Replace with actual URL if necessary
engine = create_engine(DATABASE_URL)

print(f"Database file used by script: {os.path.abspath('instance/app.db')}")

# Create an inspector to inspect the database
inspector = inspect(engine)

# Get the list of tables in the database
tables = inspector.get_table_names()

# Print the tables in the database
print("Tables in the database:", tables)

# Check if the 'users' table exists
if 'users' in tables:
    print("The 'users' table exists.")
else:
    print("The 'users' table does not exist.")





from keycloak import KeycloakAdmin

keycloak_admin = KeycloakAdmin(
    server_url="http://localhost:8080",
    username="hello",
    password="123",
    realm_name="online-learning-platform",
    client_id="flask-backend",
    client_secret_key="Okb6fbRp1JHooQp89Zk60exEUSPXUaNg",
    verify=True
)

roles = keycloak_admin.get_realm_roles()
print(roles)
