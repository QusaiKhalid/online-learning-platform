# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from protos.generated import lesson_pb2 as lesson__pb2

GRPC_GENERATED_VERSION = '1.69.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in lesson_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class LessonServiceStub(object):
    """gRPC service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetLessonById = channel.unary_unary(
                '/lesson.LessonService/GetLessonById',
                request_serializer=lesson__pb2.GetLessonRequest.SerializeToString,
                response_deserializer=lesson__pb2.Lesson.FromString,
                _registered_method=True)
        self.GetLessonsByCourse = channel.unary_unary(
                '/lesson.LessonService/GetLessonsByCourse',
                request_serializer=lesson__pb2.GetLessonsByCourseRequest.SerializeToString,
                response_deserializer=lesson__pb2.GetAllLessonsResponse.FromString,
                _registered_method=True)
        self.GetAllLessons = channel.unary_unary(
                '/lesson.LessonService/GetAllLessons',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=lesson__pb2.GetAllLessonsResponse.FromString,
                _registered_method=True)
        self.CreateLesson = channel.unary_unary(
                '/lesson.LessonService/CreateLesson',
                request_serializer=lesson__pb2.Lesson.SerializeToString,
                response_deserializer=lesson__pb2.BaseResponse.FromString,
                _registered_method=True)
        self.UpdateLesson = channel.unary_unary(
                '/lesson.LessonService/UpdateLesson',
                request_serializer=lesson__pb2.Lesson.SerializeToString,
                response_deserializer=lesson__pb2.BaseResponse.FromString,
                _registered_method=True)
        self.DeleteLesson = channel.unary_unary(
                '/lesson.LessonService/DeleteLesson',
                request_serializer=lesson__pb2.IdRequest.SerializeToString,
                response_deserializer=lesson__pb2.BaseResponse.FromString,
                _registered_method=True)


class LessonServiceServicer(object):
    """gRPC service definition
    """

    def GetLessonById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLessonsByCourse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllLessons(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateLesson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateLesson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteLesson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LessonServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetLessonById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLessonById,
                    request_deserializer=lesson__pb2.GetLessonRequest.FromString,
                    response_serializer=lesson__pb2.Lesson.SerializeToString,
            ),
            'GetLessonsByCourse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLessonsByCourse,
                    request_deserializer=lesson__pb2.GetLessonsByCourseRequest.FromString,
                    response_serializer=lesson__pb2.GetAllLessonsResponse.SerializeToString,
            ),
            'GetAllLessons': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllLessons,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=lesson__pb2.GetAllLessonsResponse.SerializeToString,
            ),
            'CreateLesson': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateLesson,
                    request_deserializer=lesson__pb2.Lesson.FromString,
                    response_serializer=lesson__pb2.BaseResponse.SerializeToString,
            ),
            'UpdateLesson': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateLesson,
                    request_deserializer=lesson__pb2.Lesson.FromString,
                    response_serializer=lesson__pb2.BaseResponse.SerializeToString,
            ),
            'DeleteLesson': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteLesson,
                    request_deserializer=lesson__pb2.IdRequest.FromString,
                    response_serializer=lesson__pb2.BaseResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'lesson.LessonService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('lesson.LessonService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class LessonService(object):
    """gRPC service definition
    """

    @staticmethod
    def GetLessonById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/GetLessonById',
            lesson__pb2.GetLessonRequest.SerializeToString,
            lesson__pb2.Lesson.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetLessonsByCourse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/GetLessonsByCourse',
            lesson__pb2.GetLessonsByCourseRequest.SerializeToString,
            lesson__pb2.GetAllLessonsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllLessons(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/GetAllLessons',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            lesson__pb2.GetAllLessonsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateLesson(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/CreateLesson',
            lesson__pb2.Lesson.SerializeToString,
            lesson__pb2.BaseResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateLesson(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/UpdateLesson',
            lesson__pb2.Lesson.SerializeToString,
            lesson__pb2.BaseResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteLesson(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/lesson.LessonService/DeleteLesson',
            lesson__pb2.IdRequest.SerializeToString,
            lesson__pb2.BaseResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
