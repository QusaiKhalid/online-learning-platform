# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from protos.generated import progress_pb2 as progress__pb2

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
        + f' but the generated code in progress_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ProgressServiceStub(object):
    """gRPC service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProgressByUserAndLesson = channel.unary_unary(
                '/progress.ProgressService/GetProgressByUserAndLesson',
                request_serializer=progress__pb2.GetProgressRequest.SerializeToString,
                response_deserializer=progress__pb2.Progress.FromString,
                _registered_method=True)
        self.GetAllProgress = channel.unary_unary(
                '/progress.ProgressService/GetAllProgress',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=progress__pb2.GetAllProgressResponse.FromString,
                _registered_method=True)
        self.CreateProgress = channel.unary_unary(
                '/progress.ProgressService/CreateProgress',
                request_serializer=progress__pb2.Progress.SerializeToString,
                response_deserializer=progress__pb2.BaseResponse.FromString,
                _registered_method=True)
        self.UpdateProgress = channel.unary_unary(
                '/progress.ProgressService/UpdateProgress',
                request_serializer=progress__pb2.Progress.SerializeToString,
                response_deserializer=progress__pb2.BaseResponse.FromString,
                _registered_method=True)
        self.DeleteProgress = channel.unary_unary(
                '/progress.ProgressService/DeleteProgress',
                request_serializer=progress__pb2.IdRequest.SerializeToString,
                response_deserializer=progress__pb2.BaseResponse.FromString,
                _registered_method=True)


class ProgressServiceServicer(object):
    """gRPC service definition
    """

    def GetProgressByUserAndLesson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProgressServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProgressByUserAndLesson': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProgressByUserAndLesson,
                    request_deserializer=progress__pb2.GetProgressRequest.FromString,
                    response_serializer=progress__pb2.Progress.SerializeToString,
            ),
            'GetAllProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllProgress,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=progress__pb2.GetAllProgressResponse.SerializeToString,
            ),
            'CreateProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProgress,
                    request_deserializer=progress__pb2.Progress.FromString,
                    response_serializer=progress__pb2.BaseResponse.SerializeToString,
            ),
            'UpdateProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProgress,
                    request_deserializer=progress__pb2.Progress.FromString,
                    response_serializer=progress__pb2.BaseResponse.SerializeToString,
            ),
            'DeleteProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProgress,
                    request_deserializer=progress__pb2.IdRequest.FromString,
                    response_serializer=progress__pb2.BaseResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'progress.ProgressService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('progress.ProgressService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ProgressService(object):
    """gRPC service definition
    """

    @staticmethod
    def GetProgressByUserAndLesson(request,
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
            '/progress.ProgressService/GetProgressByUserAndLesson',
            progress__pb2.GetProgressRequest.SerializeToString,
            progress__pb2.Progress.FromString,
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
    def GetAllProgress(request,
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
            '/progress.ProgressService/GetAllProgress',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            progress__pb2.GetAllProgressResponse.FromString,
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
    def CreateProgress(request,
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
            '/progress.ProgressService/CreateProgress',
            progress__pb2.Progress.SerializeToString,
            progress__pb2.BaseResponse.FromString,
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
    def UpdateProgress(request,
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
            '/progress.ProgressService/UpdateProgress',
            progress__pb2.Progress.SerializeToString,
            progress__pb2.BaseResponse.FromString,
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
    def DeleteProgress(request,
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
            '/progress.ProgressService/DeleteProgress',
            progress__pb2.IdRequest.SerializeToString,
            progress__pb2.BaseResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
