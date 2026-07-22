from _typeshed import Incomplete
from typing import Any, ClassVar

class BaseClaims(dict[str, Any]):  # dict values are key-dependent
    """
    Payload claims for JWT, which contains a validate interface.

    :param payload: the payload dict of JWT
    :param header: the header dict of JWT
    :param options: validate options
    :param params: other params

    An example on ``options`` parameter, the format is inspired by
    `OpenID Connect Claims`_::

        {
            "iss": {
                "essential": True,
                "values": ["https://example.com", "https://example.org"]
            },
            "sub": {
                "essential": True
                "value": "248289761001"
            },
            "jti": {
                "validate": validate_jti
            }
        }

    .. _`OpenID Connect Claims`:
        http://openid.net/specs/openid-connect-core-1_0.html#IndividualClaimsRequests
    """
    REGISTERED_CLAIMS: ClassVar[list[str]]
    header: Incomplete
    options: Incomplete
    params: Incomplete
    def __init__(self, payload, header, options=None, params=None) -> None: ...
    # TODO: Adds an attribute for each key in REGISTERED_CLAIMS
    def __getattr__(self, key: str): ...
    def get_registered_claims(self) -> dict[str, Incomplete]: ...

class JWTClaims(BaseClaims):
    def validate(self, now: int | None = None, leeway: int = 0) -> None: ...
    def validate_iss(self) -> None: ...
    def validate_sub(self) -> None: ...
    def validate_aud(self) -> None: ...
    def validate_exp(self, now: int, leeway: int) -> None: ...
    def validate_nbf(self, now: int, leeway: int) -> None: ...
    def validate_iat(self, now: int, leeway: int) -> None: ...
    def validate_jti(self) -> None: ...
