"""
authlib.oidc.rpinitiated.
~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenID Connect RP-Initiated Logout 1.0 Implementation.

https://openid.net/specs/openid-connect-rpinitiated-1_0.html
"""

from .discovery import OpenIDProviderMetadata as OpenIDProviderMetadata
from .end_session import EndSessionEndpoint as EndSessionEndpoint, EndSessionRequest as EndSessionRequest
from .registration import ClientMetadataClaims as ClientMetadataClaims

__all__ = ["EndSessionEndpoint", "EndSessionRequest", "ClientMetadataClaims", "OpenIDProviderMetadata"]
