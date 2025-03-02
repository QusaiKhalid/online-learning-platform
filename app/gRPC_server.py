import sys
import os
import logging
import grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the generated gRPC code
from protos.generated import user_pb2_grpc

# Import concrete service implementation
from app.application.gRPC_services.user_servise import UserService
from app.infrastructure.repositories.user_repository import UserRepository  # Concrete implementation

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database setup (SQLAlchemy)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')  
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def serve():
    try:
        # Create a gRPC server with a thread pool executor
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # Create a database session
        db_session = SessionLocal()

        # Create a concrete instance of the UserRepository
        user_repository = UserRepository(db_session=db_session)

        # Instantiate UserService with the concrete repository
        user_service = UserService(user_repository)

        # Add the service to the server
        user_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)

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
    serve()  # Call the serve function to start the server
