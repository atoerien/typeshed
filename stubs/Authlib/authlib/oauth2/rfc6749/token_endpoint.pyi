from _typeshed import Incomplete

from .endpoint import Endpoint

class TokenEndpoint(Endpoint):
    """
    Base class for token-based endpoints (revocation, introspection).

    Subclasses must implement :meth:`authenticate_token` and
    :meth:`create_endpoint_response`.
    """
    ENDPOINT_NAME: str | None
    SUPPORTED_TOKEN_TYPES: Incomplete
    CLIENT_AUTH_METHODS: Incomplete
    def authenticate_endpoint_client(self, request):
        """Authenticate client for endpoint with ``CLIENT_AUTH_METHODS``."""
        ...
    def authenticate_token(self, request, client):
        """Authenticate and return the token. Subclasses must implement this."""
        ...
    def create_endpoint_response(self, request):
        """Process the request and return response. Subclasses must implement this."""
        ...
