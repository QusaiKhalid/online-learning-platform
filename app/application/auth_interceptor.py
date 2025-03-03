import grpc
from flask import current_app
from app.infrastructure.keycloak_auth import keycloak_openid
from protos.generated import user_pb2

class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get("authorization", "").split(" ")[-1]  # Bearer <token>

        if not token:
            raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, "Authorization token is missing")

        try:
            # Validate token using the Flask app's configuration
            token_info = keycloak_openid.decode_token(
                token,
                key=current_app.config["KEYCLOAK_PUBLIC_KEY"],
                options={"verify_signature": True, "verify_aud": True, "verify_exp": True}
            )

            # Attach token_info to the context for further use (e.g., roles)
            handler_call_details.context.token_info = token_info

        except ValueError as e:
            raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, str(e))

        except Exception as e:
            raise grpc.RpcError(grpc.StatusCode.INTERNAL, "Internal server error during authentication")

        return continuation(handler_call_details) 