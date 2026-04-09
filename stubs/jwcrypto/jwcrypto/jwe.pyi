from _typeshed import Incomplete, SupportsKeysAndGetItem
from collections.abc import Iterable
from typing import Any
from typing_extensions import LiteralString, Self

from jwcrypto import common
from jwcrypto.common import JWException, JWSEHeaderParameter, JWSEHeaderRegistry
from jwcrypto.jwk import JWK, JWKSet

default_max_compressed_size: int
default_max_plaintext_size: int

JWEHeaderRegistry: dict[LiteralString, JWSEHeaderParameter]

default_allowed_algs: list[LiteralString]

class InvalidJWEData(JWException):
    """
    Invalid JWE Object.

    This exception is raised when the JWE Object is invalid and/or
    improperly formatted.
    """
    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

InvalidCEKeyLength = common.InvalidCEKeyLength
InvalidJWEKeyLength = common.InvalidJWEKeyLength
InvalidJWEKeyType = common.InvalidJWEKeyType
InvalidJWEOperation = common.InvalidJWEOperation

class JWE:
    """
    JSON Web Encryption object

    This object represent a JWE token.
    """
    objects: dict[str, Any]
    plaintext: bytes | None
    header_registry: JWSEHeaderRegistry
    flattened: bool
    cek: Incomplete
    decryptlog: list[str] | None
    def __init__(
        self,
        plaintext: str | bytes | None = None,
        protected: str | None = None,
        unprotected: str | None = None,
        aad: bytes | None = None,
        algs: list[LiteralString] | None = None,
        recipient: str | None = None,
        header: str | None = None,
        header_registry: (
            SupportsKeysAndGetItem[LiteralString, JWSEHeaderParameter]
            | Iterable[tuple[LiteralString, JWSEHeaderParameter]]
            | None
        ) = None,
        flattened: bool = True,
    ) -> None: ...
    @property
    def allowed_algs(self) -> list[LiteralString]: ...
    @allowed_algs.setter
    def allowed_algs(self, algs: list[LiteralString]) -> None: ...
    def add_recipient(self, key: JWK, header: dict[str, Any] | str | None = None) -> None: ...
    def serialize(self, compact: bool = False) -> str: ...
    def decrypt(self, key: JWK | JWKSet, max_plaintext: int = 0) -> None: ...
    def deserialize(self, raw_jwe: str | bytes, key: JWK | JWKSet | None = None) -> None: ...
    @property
    def payload(self) -> bytes: ...
    @property
    def jose_header(self) -> dict[Incomplete, Incomplete]: ...
    @classmethod
    def from_jose_token(cls, token: str | bytes) -> Self:
        """
        Creates a JWE object from a serialized JWE token.

        :param token: A string with the json or compat representation
         of the token.

        :raises InvalidJWEData: if the raw object is an invalid JWE token.

        :return: A JWE token
        :rtype: JWE
        """
        ...
    def __eq__(self, other: object) -> bool: ...
