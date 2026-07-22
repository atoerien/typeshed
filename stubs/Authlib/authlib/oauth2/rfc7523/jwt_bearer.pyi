from _typeshed import Incomplete
from logging import Logger
from typing import ClassVar, Final

from authlib.oauth2.rfc6749 import BaseGrant, TokenEndpointMixin

log: Logger
JWT_BEARER_GRANT_TYPE: Final[str]

class JWTBearerGrant(BaseGrant, TokenEndpointMixin):
    GRANT_TYPE = JWT_BEARER_GRANT_TYPE
    CLAIMS_OPTIONS: ClassVar[dict[str, dict[str, bool]]]
    LEEWAY: ClassVar[int]
    @staticmethod
    def sign(key, issuer, audience, subject=None, issued_at=None, expires_at=None, claims=None, **kwargs): ...
    def verify_claims(self, claims: dict[str, Incomplete]) -> None: ...
    def process_assertion_claims(self, assertion) -> dict[str, Incomplete]:
        """
        Extract JWT payload claims from request "assertion", per
        `Section 3.1`_.

        :param assertion: assertion string value in the request
        :return: JWTClaims
        :raise: InvalidGrantError

        .. _`Section 3.1`: https://tools.ietf.org/html/rfc7523#section-3.1
        """
        ...
    def extract_assertion(self, assertion: str) -> tuple[dict[str, Incomplete], Incomplete]: ...
    def validate_token_request(self) -> None:
        """
        The client makes a request to the token endpoint by sending the
        following parameters using the "application/x-www-form-urlencoded"
        format per `Section 2.1`_:

        grant_type
             REQUIRED.  Value MUST be set to
             "urn:ietf:params:oauth:grant-type:jwt-bearer".

        assertion
             REQUIRED.  Value MUST contain a single JWT.

        scope
            OPTIONAL.

        The following example demonstrates an access token request with a JWT
        as an authorization grant:

        .. code-block:: http

            POST /token.oauth2 HTTP/1.1
            Host: as.example.com
            Content-Type: application/x-www-form-urlencoded

            grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer
            &assertion=eyJhbGciOiJFUzI1NiIsImtpZCI6IjE2In0.
            eyJpc3Mi[...omitted for brevity...].
            J9l-ZhwP[...omitted for brevity...]

        .. _`Section 2.1`: https://tools.ietf.org/html/rfc7523#section-2.1
        """
        ...
    def create_token_response(self):
        """
        If valid and authorized, the authorization server issues an access
        token.
        """
        ...
    def resolve_issuer_client(self, issuer):
        """
        Fetch client via "iss" in assertion claims. Developers MUST
        implement this method in subclass, e.g.::

            def resolve_issuer_client(self, issuer):
                return Client.query_by_iss(issuer)

        :param issuer: "iss" value in assertion
        :return: Client instance
        """
        ...
    def resolve_client_public_key(self, client):
        """
        Resolve client key to decode assertion data. Developers MUST
        implement this method in subclass. For instance, there is a
        "jwks" column on client table, e.g.::

            def resolve_client_public_key(self, client):
                from joserfc import KeySet

                key_set = KeySet.import_key_set(client.jwks)
                return key_set

        :param client: instance of OAuth client model
        :return: OctKey, RSAKey, ECKey, OKPKey or KeySet instance
        """
        ...
    def authenticate_user(self, subject):
        """
        Authenticate user with the given assertion claims. Developers MUST
        implement it in subclass, e.g.::

            def authenticate_user(self, subject):
                return User.get_by_sub(subject)

        :param subject: "sub" value in claims
        :return: User instance
        """
        ...
    def get_audiences(self) -> list[str]:
        """
        Return a list of valid audience identifiers for this authorization
        server. Per RFC 7523 Section 3:

            The authorization server MUST reject any JWT that does not
            contain its own identity as the intended audience.

        Developers SHOULD implement this method to return the list of valid
        audience values, typically including the token endpoint URL and/or
        the issuer identifier. For example::

            def get_audiences(self):
                return ["https://example.com/oauth/token", "https://example.com"]

        If this method returns an empty list, audience value validation is
        skipped (only presence is checked).

        :return: list of valid audience strings
        """
        ...
    def has_granted_permission(self, client, user) -> bool:
        """
        Check if the client has permission to access the given user's resource.
        Developers MUST implement it in subclass, e.g.::

            def has_granted_permission(self, client, user):
                permission = ClientUserGrant.query(client=client, user=user)
                return permission.granted

        :param client: instance of OAuth client model
        :param user: instance of User model
        :return: bool
        """
        ...
