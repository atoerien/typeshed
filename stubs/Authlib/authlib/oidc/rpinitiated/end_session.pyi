"""
OpenID Connect RP-Initiated Logout 1.0 implementation.

https://openid.net/specs/openid-connect-rpinitiated-1_0.html
"""

from _typeshed import Incomplete
from dataclasses import dataclass

from authlib.oauth2.rfc6749.endpoint import Endpoint, EndpointRequest
from authlib.oauth2.rfc6749.requests import OAuth2Request

@dataclass
class EndSessionRequest(EndpointRequest):
    """
    Validated end session request data.

    This object is returned by :meth:`EndSessionEndpoint.validate_request`
    and contains all the validated information from the logout request.
    """
    id_token_claims: dict[Incomplete, Incomplete] | None = None
    redirect_uri: str | None = None
    logout_hint: str | None = None
    ui_locales: str | None = None
    @property
    def needs_confirmation(self) -> bool:
        """Whether user confirmation is recommended before logout."""
        ...

class EndSessionEndpoint(Endpoint):
    """
    OpenID Connect RP-Initiated Logout endpoint.

    This endpoint follows a two-phase pattern for interactive flows:

    1. Call ``server.validate_endpoint_request("end_session")`` to validate
       the request and get an :class:`EndSessionRequest`
    2. Check ``end_session_request.needs_confirmation`` and show UI if needed
    3. Call ``server.create_endpoint_response("end_session", end_session_request)``
       to execute logout and create the response

    Example usage::

        class MyEndSessionEndpoint(EndSessionEndpoint):
            def get_server_jwks(self):
                return load_jwks()

            def end_session(self, end_session_request):
                session.clear()


        server.register_endpoint(MyEndSessionEndpoint)


        @app.route("/logout", methods=["GET", "POST"])
        def logout():
            try:
                req = server.validate_endpoint_request("end_session")
            except OAuth2Error as error:
                return server.handle_error_response(None, error)

            if req.needs_confirmation and request.method == "GET":
                return render_template("confirm_logout.html", client=req.client)

            return server.create_endpoint_response(
                "end_session", req
            ) or render_template("logged_out.html")

    For non-interactive usage (no confirmation page), use the standard pattern::

        @app.route("/logout", methods=["GET", "POST"])
        def logout():
            return server.create_endpoint_response("end_session") or render_template(
                "logged_out.html"
            )
    """
    ENDPOINT_NAME: str
    def validate_request(self, request: OAuth2Request) -> EndSessionRequest:
        """
        Validate an end session request.

        :param request: The OAuth2Request to validate
        :returns: EndSessionRequest with validated data
        :raises InvalidRequestError: If validation fails
        """
        ...
    def create_response(self, validated_request: EndSessionRequest) -> tuple[int, Incomplete, list[tuple[str, str]]] | None:
        """
        Create the end session HTTP response.

        Executes the logout via :meth:`end_session`, then returns a redirect
        response if a valid redirect_uri is present, or None to let the
        application provide its own response.

        :param validated_request: The validated EndSessionRequest
        :returns: Tuple of (status_code, body, headers) for redirect, or None
        """
        ...
    def resolve_client_from_id_token_claims(self, id_token_claims: dict[Incomplete, Incomplete]) -> Incomplete | None:
        """
        Resolve client from id_token aud claim.

        When aud is a single string, resolves the client directly.
        When aud is a list, returns None (ambiguous case).
        Override for custom resolution logic.
        """
        ...
    def is_post_logout_redirect_uri_legitimate(
        self, request: OAuth2Request, post_logout_redirect_uri: str, client, logout_hint: str | None
    ) -> bool:
        """
        Confirm redirect_uri legitimacy when no id_token_hint is provided.

        Override if you have alternative confirmation mechanisms, e.g.::

            def is_post_logout_redirect_uri_legitimate(self, ...):
                return client and client.is_trusted

        By default returns False (no redirection without id_token_hint).
        """
        ...
    def get_server_jwks(self):
        """Return the server's JSON Web Key Set for validating ID tokens."""
        ...
    def get_algorithms(self) -> list[str]:
        """
        Return the list of allowed algorithms for ID token validation.

        By default, returns all algorithms compatible with the keys in the JWKS.
        Override to restrict to specific algorithms.
        """
        ...
    def end_session(self, end_session_request: EndSessionRequest) -> None:
        """
        Terminate the user's session.

        Implement this method to perform the actual logout logic,
        such as clearing session data, revoking tokens, etc.

        Use ``end_session_request.logout_hint`` to help identify the user
        (e.g. email, username) when no ``id_token_hint`` is provided.

        :param end_session_request: The validated EndSessionRequest
        """
        ...
