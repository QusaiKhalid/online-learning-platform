import sys
import os
import grpc
import requests  # For making HTTP requests to Keycloak

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos.generated import user_pb2, user_pb2_grpc

# Create a gRPC channel to the server
channel = grpc.insecure_channel('localhost:50051')  # Connect to the server on port 50051

# Create a stub (client)
stub = user_pb2_grpc.UserServiceStub(channel)

# Function to authenticate with Keycloak and retrieve an access token
def get_access_token(username: str, password: str) -> str:
    """
    Authenticate with Keycloak and return an access token.
    """
    login_url = "http://localhost:50051/auth/login"  # Replace with your actual login endpoint
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, json=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to authenticate: {response.text}")

# Example: Test GetUserById
def test_get_user_by_id(user_id, access_token):
    try:
        # Create the request
        request = user_pb2.GetUserRequest(id=user_id)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = stub.GetUserById(request, metadata=metadata)

        # Check the response
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with ID {user_id} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test GetUserByEmail
def test_get_user_by_email(user_email, access_token):
    try:
        request = user_pb2.GetUserByEmailRequest(email=user_email)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = stub.GetUserByEmail(request, metadata=metadata)
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with email {user_email} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test CreateUser with an optional role
def test_create_user(email, username, password, role=None, access_token=None):
    try:
        request = user_pb2.CreateUserRequest(
            email=email,
            username=username,
            password=password,
            role=role 
        )

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')] if access_token else None

        # Make the gRPC call with metadata
        response = stub.CreateUser(request, metadata=metadata)
        print(f"CreateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test UpdateUser
def test_update_user(user_id, email, username, access_token):
    try:
        request = user_pb2.UpdateUserRequest(
            id=user_id,
            email=email,
            username=username
        )

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = stub.UpdateUser(request, metadata=metadata)
        print(f"UpdateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test DeleteUser
def test_delete_user(user_id, access_token):
    try:
        request = user_pb2.IdRequest(id=user_id)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = stub.DeleteUser(request, metadata=metadata)
        print(f"DeleteUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Authenticate and obtain an access token
    try:
        username = "qusai"  # Replace with a valid username
        password = "123"  # Replace with a valid password
        access_token = get_access_token(username, password)
        print(f"Access token obtained successfully: {access_token[:20]}...")  # Print a truncated token
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        exit(1)

    # Example test cases
    test_create_user("newuser2@example.com", "newuser2", "password123", access_token=access_token)  # Create a new user
    # test_get_user_by_id(2, access_token=access_token)  # Replace with an actual user ID
    # test_get_user_by_email("updatedemail@example.com", access_token=access_token)  # Replace with an actual email
    # test_update_user(2, "updatedemail1@example.com", "updatedusername1", access_token=access_token)  # Replace with actual user ID
    # test_delete_user(2, access_token=access_token)  # Replace with an actual user ID