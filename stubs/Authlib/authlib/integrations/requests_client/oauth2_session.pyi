from _typeshed import Incomplete

from authlib.oauth2.auth import ClientAuth, TokenAuth
from authlib.oauth2.client import OAuth2Client

from ..base_client import OAuthError

__all__ = ["OAuth2Session", "OAuth2Auth"]

# Inherits from requests.auth.AuthBase
class OAuth2Auth(TokenAuth):
    """Sign requests for OAuth 2.0, currently only bearer token is supported."""
    def ensure_active_token(self) -> None: ...
    def __call__(self, req): ...

# Inherits from requests.auth.AuthBase
class OAuth2ClientAuth(ClientAuth):
    """Attaches OAuth Client Authentication to the given Request object."""
    def __call__(self, req): ...

# Inherits from requests.Session
class OAuth2Session(OAuth2Client):
    """
    Construct a new OAuth 2 client requests session.

    :param client_id: Client ID, which you get from client registration.
    :param client_secret: Client Secret, which you get from registration.
    :param authorization_endpoint: URL of the authorization server's
        authorization endpoint.
    :param token_endpoint: URL of the authorization server's token endpoint.
    :param token_endpoint_auth_method: client authentication method for
        token endpoint.
    :param revocation_endpoint: URL of the authorization server's OAuth 2.0
        revocation endpoint.
    :param revocation_endpoint_auth_method: client authentication method for
        revocation endpoint.
    :param scope: Scope that you needed to access user resources.
    :param state: Shared secret to prevent CSRF attack.
    :param redirect_uri: Redirect URI you registered as callback.
    :param token: A dict of token attributes such as ``access_token``,
        ``token_type`` and ``expires_at``.
    :param token_placement: The place to put token in HTTP request. Available
        values: "header", "body", "uri".
    :param update_token: A function for you to update token. It accept a
        :class:`OAuth2Token` as parameter.
    :param leeway: Time window in seconds before the actual expiration of the
        authentication token, that the token is considered expired and will
        be refreshed.
    :param default_timeout: If settled, every requests will have a default timeout.
    """
    client_auth_class = OAuth2ClientAuth
    token_auth_class = OAuth2Auth
    oauth_error_class = OAuthError  # type: ignore[assignment]
    SESSION_REQUEST_PARAMS: tuple[str, ...]  # type: ignore[assignment]
    default_timeout: Incomplete
    def __init__(
        self,
        client_id=None,
        client_secret=None,
        token_endpoint_auth_method=None,
        revocation_endpoint_auth_method=None,
        scope=None,
        state=None,
        redirect_uri=None,
        token=None,
        token_placement="header",
        update_token=None,
        leeway=60,
        default_timeout=None,
        **kwargs,
    ) -> None: ...
    def fetch_access_token(self, url=None, **kwargs):
        """Alias for fetch_token."""
        ...
    def request(self, method, url, withhold_token=False, auth=None, **kwargs):
        """Send request with auto refresh token feature (if available)."""
        ...
