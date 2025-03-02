from protos.generated import user_pb2

def user_to_proto(user):
    return user_pb2.GetUserResponse(
        id=user.id,
        email=user.email,
        username=user.username
    )

def success_response(message):
    return user_pb2.BaseResponse(success=True, message=message)
