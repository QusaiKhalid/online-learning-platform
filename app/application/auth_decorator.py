from functools import wraps
from app.infrastructure.keycloak_auth import keycloak_openid  # Import Keycloak client

def authenticate_grpc_method(func):
    """
    Decorator to validate tokens for gRPC methods.
    """
    @wraps(func)
    def wrapper(self, request, context):
        try:
            # Extract token from metadata
            metadata = dict(context.invocation_metadata())
            token = metadata.get("authorization", "").split(" ")[-1]  # Bearer <token>

            if not token:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Authorization token is missing")
                return None

            # Validate token
            token_info = keycloak_openid.decode_token(
                token,
                key=self.app.config["KEYCLOAK_PUBLIC_KEY"],  # Optional: Use Keycloak's public key
                options={"verify_signature": True, "verify_aud": True, "verify_exp": True}
            )

            # Attach token_info to the context for further use (e.g., roles)
            context.token_info = token_info

            # Call the original method
            return func(self, request, context)

        except ValueError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(e))
            return None
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error during authentication")
            return None

    return wrapper