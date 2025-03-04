import sys
import os
import logging
import grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Import the generated gRPC code
from app.config import Config
from protos.generated import user_pb2_grpc
from protos.generated import auth_pb2_grpc

# Import concrete service implementation
from app.application.gRPC_services.user_servise import UserService
from app.application.gRPC_services.auth_service import AuthServicer

from app.infrastructure.repositories.user_repository import UserRepository  # Concrete implementation

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Debugging: Log the environment variable and constructed database URL
# Use the database URL from the Config class
DATABASE_URL = "sqlite:///C:/Internship/1st Task/online-learning-platform/instance/app.db"
logging.debug(f"Using DATABASE_URL: {DATABASE_URL}")

# Ensure the directory exists
if not os.path.exists('instance'):
    os.makedirs('instance')
    logging.debug("Created 'instance' directory.")



# Database setup (SQLAlchemy)
try:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logging.debug("Database engine created successfully.")
except Exception as e:
    logging.error(f"Error creating database engine: {str(e)}")

def serve():
    try:
        # Create a gRPC server with a thread pool executor
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # Debugging: Log the creation of a session
        db_session = SessionLocal()
        logging.debug("Created new database session.")

        # Create a concrete instance of the UserRepository
        user_repository = UserRepository(db_session=db_session)

        # Instantiate UserService with the concrete repository
        user_service = UserService(user_repository)

        # Add the service to the server
        user_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)

        # Add Auth Service
        auth_service = AuthServicer()
        auth_pb2_grpc.add_AuthServiceServicer_to_server(auth_service, server)

        # Specify the address and port to listen on
        server.add_insecure_port('[::]:50051')  # Listens on all interfaces on port 50051

        # Start the server
        server.start()
        logging.info("Server is running on port 50051...")

        # Keep the server running
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"Error starting the server: {str(e)}")

if __name__ == '__main__':
    logging.debug("Starting server...")
    serve()  # Call the serve function to start the server