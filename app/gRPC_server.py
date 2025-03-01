import grpc
from concurrent import futures

# Import the generated gRPC code
from protos.generated import user_pb2_grpc, progress_pb2_grpc, lesson_pb2_grpc, enrollment_pb2_grpc, course_pb2_grpc

# Import your service implementations
from app.application.services.user_servise import UserService
from app.application.services.progress_servise import ProgressService
from app.application.services.lesson_servise import LessonService
from app.application.services.enrollment_servise import EnrollmentService
from app.application.services.course_servise import CourseService

def serve():
    # Create a gRPC server with a thread pool executor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add your services to the server
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    progress_pb2_grpc.add_ProgressServiceServicer_to_server(ProgressService(), server)
    lesson_pb2_grpc.add_LessonServiceServicer_to_server(LessonService(), server)
    enrollment_pb2_grpc.add_EnrollmentServiceServicer_to_server(EnrollmentService(), server)
    course_pb2_grpc.add_CourseServiceServicer_to_server(CourseService(), server)

    # Specify the address and port to listen on
    server.add_insecure_port('[::]:50051')  # Listens on all interfaces on port 50051
    server.start()  # Start the server
    print("Server is running on port 50051...")
    server.wait_for_termination()  # Keep the server running


    
if __name__ == '__main__':
    serve()  # Call the serve function to start the server