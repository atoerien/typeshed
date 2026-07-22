from _typeshed import Incomplete
from logging import Logger
from typing import Final, overload
from typing_extensions import deprecated

ASSERTION_TYPE: Final[str]
log: Logger

class JWTBearerClientAssertion:
    """
    Implementation of Using JWTs for Client Authentication, which is
    defined by RFC7523.
    """
    CLIENT_ASSERTION_TYPE: Final[str]
    CLIENT_AUTH_METHOD: Final[str]
    token_url: str | None
    leeway: int

    @overload
    @deprecated("The `token_url` parameter is deprecated. Override `get_audiences` instead.")
    def __init__(self, token_url: str = ..., validate_jti: bool = True, leeway: int = 60) -> None: ...
    @overload
    def __init__(self, token_url: None = None, validate_jti: bool = True, leeway: int = 60) -> None: ...

    def __call__(self, query_client, request): ...
    def verify_claims(self, claims: dict[str, Incomplete]) -> None: ...
    def get_audiences(self) -> list[str]:
        """
        Return a list of valid audience identifiers for this authorization
        server. Per RFC 7523 Section 3, the audience identifies the
        authorization server as an intended audience.

        Developers MUST implement this method::

            def get_audiences(self):
                return ["https://example.com/oauth/token", "https://example.com"]

        :return: list of valid audience strings
        """
        ...
    def process_assertion_claims(self, assertion, resolve_key) -> dict[str, Incomplete]:
        """
        Extract JWT payload claims from request "assertion", per
        `Section 3.1`_.

        :param assertion: assertion string value in the request
        :param resolve_key: function to resolve the sign key
        :return: JWTClaims
        :raise: InvalidClientError

        .. _`Section 3.1`: https://tools.ietf.org/html/rfc7523#section-3.1
        """
        ...
    def authenticate_client(self, client): ...
    def extract_assertion(self, assertion: str) -> tuple[dict[str, Incomplete], Incomplete]: ...
    def validate_jti(self, claims, jti):
        """
        Validate if the given ``jti`` value is used before. Developers
        MUST implement this method::

            def validate_jti(self, claims, jti):
                key = "jti:{}-{}".format(claims["sub"], jti)
                if redis.get(key):
                    return False
                redis.set(key, 1, ex=3600)
                return True
        """
        ...
    def resolve_client_public_key(self, client):
        """
        Resolve the client public key for verifying the JWT signature.
        Developers MUST implement this method::

            from joserfc.jwk import KeySet


            def resolve_client_public_key(self, client):
                return KeySet.import_key_set(client.public_jwks)
        """
        ...
