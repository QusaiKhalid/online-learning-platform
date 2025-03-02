import sys
import os
import grpc
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos.generated import user_pb2, user_pb2_grpc

# Create a gRPC channel to the server
channel = grpc.insecure_channel('localhost:50051')  # Connect to the server on port 50051

# Create a stub (client)
stub = user_pb2_grpc.UserServiceStub(channel)

# Example: Test GetUserById
def test_get_user_by_id(user_id):
    try:
        # Create the request
        request = user_pb2.GetUserRequest(id=user_id)

        # Make the gRPC call
        response = stub.GetUserById(request)

        # Check the response
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with ID {user_id} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test GetUserByEmail
def test_get_user_by_email(user_email):
    try:
        request = user_pb2.GetUserByEmailRequest(email=user_email)
        response = stub.GetUserByEmail(request)
        if response.id != 0:
            print(f"User found: ID={response.id}, Email={response.email}, Username={response.username}")
        else:
            print(f"User with email {user_email} not found.")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test CreateUser with an optional role
def test_create_user(email, username, password, role=None):
    try:
        request = user_pb2.CreateUserRequest(
            email=email,
            username=username,
            password=password,
            role=role 
        )
        response = stub.CreateUser(request)
        print(f"CreateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test UpdateUser
def test_update_user(user_id, email, username):
    try:
        request = user_pb2.UpdateUserRequest(
            id=user_id,
            email=email,
            username=username
        )
        response = stub.UpdateUser(request)
        print(f"UpdateUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

# Example: Test DeleteUser
def test_delete_user(user_id):
    try:
        request = user_pb2.IdRequest(id=user_id)
        response = stub.DeleteUser(request)
        print(f"DeleteUser response: success={response.success}, message={response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Example test cases:
      test_create_user("newuser1@example.com", "newuser1", "password123")  # Create a new user
    #  test_get_user_by_id(2)  # Replace with an actual user ID
    # test_get_user_by_email("updatedemail@example.com")  # Replace with an actual email
    #  test_update_user(2, "updatedemail1@example.com", "updatedusername1")  # Replace with actual user ID
    #  test_delete_user(2)  # Replace with an actual user ID
