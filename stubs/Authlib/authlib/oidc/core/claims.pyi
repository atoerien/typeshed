from collections.abc import Callable

from authlib.jose import JWTClaims

__all__ = ["IDToken", "CodeIDToken", "ImplicitIDToken", "HybridIDToken", "UserInfo", "get_claim_cls_by_response_type"]

class IDToken(JWTClaims):
    ESSENTIAL_CLAIMS: list[str]
    def validate(self, now: int | Callable[[], int] | None = None, leeway: int = 0) -> None: ...
    def validate_auth_time(self) -> None: ...
    def validate_nonce(self) -> None: ...
    def validate_amr(self) -> None: ...
    def validate_azp(self) -> None: ...
    def validate_at_hash(self) -> None: ...

class CodeIDToken(IDToken):
    RESPONSE_TYPES: tuple[str, ...]

class ImplicitIDToken(IDToken):
    RESPONSE_TYPES: tuple[str, ...]
    ESSENTIAL_CLAIMS: list[str]
    def validate_at_hash(self) -> None:
        """
        If the ID Token is issued from the Authorization Endpoint with an
        access_token value, which is the case for the response_type value
        id_token token, this is REQUIRED; it MAY NOT be used when no Access
        Token is issued, which is the case for the response_type value
        id_token.
        """
        ...

class HybridIDToken(ImplicitIDToken):
    RESPONSE_TYPES: tuple[str, ...]
    def validate(self, now=None, leeway: int = 0) -> None: ...
    def validate_c_hash(self) -> None:
        """
        Code hash value. Its value is the base64url encoding of the
        left-most half of the hash of the octets of the ASCII representation
        of the code value, where the hash algorithm used is the hash algorithm
        used in the alg Header Parameter of the ID Token's JOSE Header. For
        instance, if the alg is HS512, hash the code value with SHA-512, then
        take the left-most 256 bits and base64url encode them. The c_hash
        value is a case sensitive string.
        If the ID Token is issued from the Authorization Endpoint with a code,
        which is the case for the response_type values code id_token and code
        id_token token, this is REQUIRED; otherwise, its inclusion is OPTIONAL.
        """
        ...

class UserInfo(dict[str, object]):
    """
    The standard claims of a UserInfo object. Defined per `Section 5.1`_.

    .. _`Section 5.1`: http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
    """
    REGISTERED_CLAIMS: list[str]
    SCOPES_CLAIMS_MAPPING: dict[str, list[str]]
    def filter(self, scope: str) -> UserInfo:
        """Return a new UserInfo object containing only the claims matching the scope passed in parameter."""
        ...
    def __getattr__(self, key): ...

def get_claim_cls_by_response_type(response_type) -> type: ...
