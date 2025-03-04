from protos.generated import user_pb2

def user_to_proto(user):
    if not user:
        return user_pb2.GetUserResponse(message="User not found")  # Return a valid protobuf message
    return user_pb2.GetUserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role,
        message="User retrieved successfully"
    )

def success_response(message):
    return user_pb2.BaseResponse(success=True, message=message)
