from authlib.oauth2.rfc7009 import RevocationEndpoint as _RevocationEndpoint

class RevocationEndpoint(_RevocationEndpoint):
    """
    The revocation endpoint for OAuth authorization servers allows clients
    to notify the authorization server that a previously obtained refresh or
    access token is no longer needed.

    Register it into authorization server, and create token endpoint response
    for token revocation::

        from django.views.decorators.http import require_http_methods

        # see register into authorization server instance
        server.register_endpoint(RevocationEndpoint)


        @require_http_methods(["POST"])
        def revoke_token(request):
            return server.create_endpoint_response(
                RevocationEndpoint.ENDPOINT_NAME, request
            )
    """
    def query_token(self, token, token_type_hint):
        """Query requested token from database."""
        ...
    def revoke_token(self, token, request) -> None:
        """Mark the give token as revoked."""
        ...
