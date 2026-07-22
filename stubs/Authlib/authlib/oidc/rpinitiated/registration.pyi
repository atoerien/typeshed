"""
Client metadata for OpenID Connect RP-Initiated Logout 1.0.

https://openid.net/specs/openid-connect-rpinitiated-1_0.html
"""

from collections.abc import Callable

from authlib.oauth2.claims import BaseClaims

class ClientMetadataClaims(BaseClaims):
    """
    Client metadata for OpenID Connect RP-Initiated Logout 1.0.

    This can be used with :ref:`specs/rfc7591` and :ref:`specs/rfc7592` endpoints::

        server.register_endpoint(
            ClientRegistrationEndpoint(
                claims_classes=[
                    rfc7591.ClientMetadataClaims,
                    oidc.registration.ClientMetadataClaims,
                    oidc.rpinitiated.ClientMetadataClaims,
                ]
            )
        )
    """
    REGISTERED_CLAIMS: list[str]
    def validate(self, now: int | Callable[[], int] | None = None, leeway: int = 0) -> None: ...
