import sys
import os
import grpc

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import generated gRPC code for UserService and AuthService
from protos.generated import user_pb2, user_pb2_grpc, auth_pb2, auth_pb2_grpc
from google.protobuf import empty_pb2  # Import for Empty message

# Create gRPC channels to the server
user_channel = grpc.insecure_channel('localhost:50051')  # Connect to the server on port 50051
auth_channel = grpc.insecure_channel('localhost:50051')  # Same server for AuthService

# Create stubs (clients)
user_stub = user_pb2_grpc.UserServiceStub(user_channel)
auth_stub = auth_pb2_grpc.AuthServiceStub(auth_channel)

# Function to authenticate with Keycloak using gRPC AuthService
def get_access_token(username: str, password: str) -> str:
    """
    Authenticate with Keycloak via gRPC AuthService and return an access token.
    """
    try:
        # Create the LoginRequest
        request = auth_pb2.LoginRequest(username=username, password=password)

        # Call the Login method on the AuthService stub
        response = auth_stub.Login(request)

        # Extract and return the access token
        return response.access_token
    except grpc.RpcError as e:
        print(f"gRPC error during authentication: {e.code()} - {e.details()}")
        raise Exception(f"Failed to authenticate: {e.details()}")

# Example: Test GetUserById
def test_get_user_by_id(user_id, access_token):
    try:
        # Create the request
        request = user_pb2.GetUserRequest(id=user_id)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = user_stub.GetUserById(request, metadata=metadata)

        # Check the response
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with ID {user_id} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test GetUserByEmail
def test_get_user_by_email(email, access_token):
    try:
        # Create the request
        request = user_pb2.GetUserByEmailRequest(email=email)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = user_stub.GetUserByEmail(request, metadata=metadata)

        # Check the response
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with email {email} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test CreateUser with an optional role
def test_create_user(email, username, password, role=None, access_token=None):
    try:
        # Create the request
        request = user_pb2.CreateUserRequest(
            email=email,
            username=username,
            password=password,
            role=role
        )

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')] if access_token else None

        # Make the gRPC call with metadata
        response = user_stub.CreateUser(request, metadata=metadata)

        # Print the response
        print(f"CreateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test UpdateUser
def test_update_user(user_id, email, username, access_token):
    try:
        # Create the request
        request = user_pb2.UpdateUserRequest(
            id=user_id,
            email=email,
            username=username
        )

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = user_stub.UpdateUser(request, metadata=metadata)

        # Print the response
        print(f"UpdateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test DeleteUser
def test_delete_user(user_id, access_token):
    try:
        # Create the request
        request = user_pb2.IdRequest(id=user_id)

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = user_stub.DeleteUser(request, metadata=metadata)

        # Print the response
        print(f"DeleteUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test GetAllUsers
def test_get_all_users(access_token):
    try:
        # Create the request (Empty message for GetAllUsers)
        request = empty_pb2.Empty()

        # Include the token in metadata
        metadata = [('authorization', f'Bearer {access_token}')]

        # Make the gRPC call with metadata
        response = user_stub.GetAllUsers(request, metadata=metadata)

        # Print the response
        if response.users:
            print("All Users:")
            for user in response.users:
                print(f"ID={user.id}, Email={user.email}, Username={user.username}, Role={user.role}")
        else:
            print("No users found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Authenticate and obtain an access token using gRPC AuthService
    try:
        username = "qusai"  # Replace with a valid username
        password = "123"  # Replace with a valid password
        access_token = get_access_token(username, password)
        print(f"Access token obtained successfully: {access_token[:20]}...")  # Print a truncated token
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        exit(1)

    # Example test cases
    # test_create_user("newuser3@example.com", "newuser3", "password123", access_token=access_token)  # Create a new user
    test_get_user_by_id(9, access_token=access_token)  # Replace with an actual user ID
    # test_get_user_by_email("newuser7@example.com", access_token=access_token)  # Replace with an actual email
    # test_update_user(2, "updatedemail1@example.com", "updatedusername1", access_token=access_token)  # Replace with actual user ID
    # test_delete_user(2, access_token=access_token)  # Replace with an actual user ID
    # test_get_all_users(access_token)  # Fetch all users