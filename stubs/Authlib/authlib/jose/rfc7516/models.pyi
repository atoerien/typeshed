from _typeshed import Incomplete
from abc import ABCMeta
from collections.abc import Iterable, Sized
from typing import ClassVar
from typing_extensions import Self

class JWEAlgorithmBase(metaclass=ABCMeta):
    """Base interface for all JWE algorithms."""
    EXTRA_HEADERS: ClassVar[Iterable[str] | None]
    name: str | None
    description: str | None
    deprecated: bool
    algorithm_type: str
    algorithm_location: str
    def prepare_key(self, raw_data): ...
    def generate_preset(self, enc_alg, key): ...

class JWEAlgorithm(JWEAlgorithmBase, metaclass=ABCMeta):
    """
    Interface for JWE algorithm conforming to RFC7518.
    JWA specification (RFC7518) SHOULD implement the algorithms for JWE
    with this base implementation.
    """
    def wrap(self, enc_alg, headers, key, preset=None): ...
    def unwrap(self, enc_alg, ek, headers, key): ...

class JWEAlgorithmWithTagAwareKeyAgreement(JWEAlgorithmBase, metaclass=ABCMeta):
    """
    Interface for JWE algorithm with tag-aware key agreement (in key agreement
    with key wrapping mode).
    ECDH-1PU is an example of such an algorithm.
    """
    def generate_keys_and_prepare_headers(self, enc_alg, key, sender_key, preset=None): ...
    def agree_upon_key_and_wrap_cek(self, enc_alg, headers, key, sender_key, epk, cek, tag): ...
    def wrap(self, enc_alg, headers, key, sender_key, preset=None): ...
    def unwrap(self, enc_alg, ek, headers, key, sender_key, tag=None): ...

class JWEEncAlgorithm:
    name: str | None
    description: str | None
    algorithm_type: str
    algorithm_location: str
    IV_SIZE: int | None
    CEK_SIZE: int | None
    def generate_cek(self) -> bytes: ...
    def generate_iv(self) -> bytes: ...
    def check_iv(self, iv: Sized) -> None: ...
    def encrypt(self, msg, aad, iv, key) -> tuple[bytes, bytes]:
        """
        Encrypt the given "msg" text.

        :param msg: text to be encrypt in bytes
        :param aad: additional authenticated data in bytes
        :param iv: initialization vector in bytes
        :param key: encrypted key in bytes
        :return: (ciphertext, tag)
        """
        ...
    def decrypt(self, ciphertext, aad, iv, tag, key) -> bytes:
        """
        Decrypt the given cipher text.

        :param ciphertext: ciphertext in bytes
        :param aad: additional authenticated data in bytes
        :param iv: initialization vector in bytes
        :param tag: authentication tag in bytes
        :param key: encrypted key in bytes
        :return: message
        """
        ...

class JWEZipAlgorithm:
    name: Incomplete
    description: Incomplete
    algorithm_type: str
    algorithm_location: str
    def compress(self, s: bytes) -> bytes | None: ...
    def decompress(self, s: bytes) -> bytes | None: ...

class JWESharedHeader(dict[str, object]):
    """
    Shared header object for JWE.

    Combines protected header and shared unprotected header together.
    """
    protected: Incomplete
    unprotected: Incomplete
    def __init__(self, protected, unprotected) -> None: ...
    def update_protected(self, addition) -> None: ...
    @classmethod
    def from_dict(cls, obj) -> Self: ...

class JWEHeader(dict[str, object]):
    """
    Header object for JWE.

    Combines protected header, shared unprotected header
    and specific recipient's unprotected header together.
    """
    protected: Incomplete
    unprotected: Incomplete
    header: Incomplete
    def __init__(self, protected, unprotected, header) -> None: ...
