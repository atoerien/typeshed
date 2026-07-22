from _typeshed import Incomplete

from ..rfc7662 import IntrospectionEndpoint
from .claims import JWTAccessTokenClaims

class JWTIntrospectionEndpoint(IntrospectionEndpoint):
    r"""
    JWTIntrospectionEndpoint inherits from :ref:`specs/rfc7662`
    :class:`~authlib.oauth2.rfc7662.IntrospectionEndpoint` and implements the machinery
    to automatically process the JWT access tokens.

    :param issuer: The issuer identifier for which tokens will be introspected.

    :param \\*\\*kwargs: Other parameters are inherited from
        :class:`~authlib.oauth2.rfc7662.introspection.IntrospectionEndpoint`.

    ::

        class MyJWTAccessTokenIntrospectionEndpoint(JWTIntrospectionEndpoint):
            def get_jwks(self): ...

            def get_username(self, user_id): ...


        # endpoint dedicated to JWT access token introspection
        authorization_server.register_endpoint(
            MyJWTAccessTokenIntrospectionEndpoint(
                issuer="https://authorization-server.example.org",
            )
        )

        # another endpoint dedicated to refresh token introspection
        authorization_server.register_endpoint(MyRefreshTokenIntrospectionEndpoint)
    """
    ENDPOINT_NAME: str
    issuer: Incomplete
    def __init__(self, issuer, server=None, *args, **kwargs) -> None: ...
    def create_endpoint_response(self, request): ...
    def authenticate_token(self, request, client) -> JWTAccessTokenClaims | None: ...
    def create_introspection_payload(self, token: JWTAccessTokenClaims) -> dict[str, Incomplete]: ...
    def get_jwks(self): ...
    def get_username(self, user_id: str) -> str: ...
