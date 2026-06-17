from _typeshed import StrOrBytesPath, SupportsWrite
from pathlib import Path
from re import Pattern
from typing import Final, NamedTuple, Protocol, TypeAlias, TypeVar, type_check_only
from typing_extensions import Self

from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat
from paramiko.message import Message

@type_check_only
class _HasReadlines(Protocol):
    def readlines(self) -> list[str]: ...

OPENSSH_AUTH_MAGIC: bytes

_BytesT = TypeVar("_BytesT", bound=bytes | bytearray)

def _unpad_openssh(data: _BytesT) -> _BytesT: ...

class UnknownKeyType(Exception):
    """An unknown public/private key algorithm was attempted to be read."""
    key_type: str | type | None
    key_bytes: bytes | None
    def __init__(self, key_type: str | type | None = None, key_bytes: bytes | None = None) -> None: ...

class FileFormat(NamedTuple):
    format: PrivateFormat
    encoding: Encoding

PrivateKey: TypeAlias = RSAPrivateKey | EllipticCurvePrivateKey | Ed25519PrivateKey

PEM: Final[FileFormat]
OPENSSH: Final[FileFormat]

class PKey:
    public_blob: PublicBlob | None
    BEGIN_TAG: Pattern[str]
    END_TAG: Pattern[str]
    @staticmethod
    def from_path(path: Path | str, password: str | None = None) -> PKey: ...
    @staticmethod
    def from_type_string(key_type: str, key_bytes: bytes, password: str | None = None) -> PKey: ...
    @classmethod
    def identifiers(cls) -> list[str]:
        """
        returns an iterable of key format/name strings this class can handle.

        Most classes only have a single identifier, and thus this default
        implementation suffices; see `.ECDSAKey` for one example of an
        override.
        """
        ...
    def __init__(self, msg: Message | None = None, data: str | None = None) -> None:
        """
        Create a new instance of this public key type.  If ``msg`` is given,
        the key's public part(s) will be filled in from the message.  If
        ``data`` is given, the key's public part(s) will be filled in from
        the string.

        :param .Message msg:
            an optional SSH `.Message` containing a public key of this type.
        :param bytes data:
            optional, the bytes of a public key of this type

        :raises: `.SSHException` --
            if a key cannot be created from the ``data`` or ``msg`` given, or
            no key was passed in.
        """
        ...
    def asbytes(self) -> bytes:
        """
        Return a string of an SSH `.Message` made up of the public part(s) of
        this key.  This string is suitable for passing to `__init__` to
        re-create the key object later.
        """
        ...
    def __bytes__(self) -> bytes: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def get_name(self) -> str:
        """
        Return the name of this private key implementation.

        :return:
            name of this private key type, in SSH terminology, as a `str` (for
            example, ``"ssh-rsa"``).
        """
        ...
    @property
    def algorithm_name(self) -> str:
        """
        Return the key algorithm identifier for this key.

        Similar to `get_name`, but aimed at pure algorithm name instead of SSH
        protocol field value.
        """
        ...
    def get_bits(self) -> int:
        """
        Return the number of significant bits in this key.  This is useful
        for judging the relative security of a key.

        :return: bits in the key (as an `int`)
        """
        ...
    def can_sign(self) -> bool:
        """
        Return ``True`` if this key has the private part necessary for signing
        data.
        """
        ...
    def get_fingerprint(self) -> bytes:
        """
        Return an MD5 fingerprint of the public part of this key.  Nothing
        secret is revealed.

        :return:
            a 16-byte `string <str>` (binary) of the MD5 fingerprint, in SSH
            format.
        """
        ...
    @property
    def fingerprint(self) -> str:
        """
        Modern fingerprint property designed to be comparable to OpenSSH.

        Currently only does SHA256 (the OpenSSH default).

        .. versionadded:: 3.2
        """
        ...
    def get_base64(self) -> str:
        """
        Return a base64 string containing the public part of this key.  Nothing
        secret is revealed.  This format is compatible with that used to store
        public key files or recognized host keys.

        :return: a base64 `string <str>` containing the public part of the key.
        """
        ...
    def sign_ssh_data(self, data: bytes, algorithm: str | None = None) -> Message:
        """
        Sign a blob of data with this private key, and return a `.Message`
        representing an SSH signature message.

        :param bytes data:
            the data to sign.
        :param str algorithm:
            the signature algorithm to use, if different from the key's
            internal name. Default: ``None``.
        :return: an SSH signature `message <.Message>`.

        .. versionchanged:: 2.9
            Added the ``algorithm`` kwarg.
        """
        ...
    def verify_ssh_sig(self, data: bytes, msg: Message) -> bool:
        """
        Given a blob of data, and an SSH message representing a signature of
        that data, verify that it was signed with this key.

        :param bytes data: the data that was signed.
        :param .Message msg: an SSH signature message
        :return:
            ``True`` if the signature verifies correctly; ``False`` otherwise.
        """
        ...
    @classmethod
    def from_private_key_file(cls, filename: StrOrBytesPath, password: str | None = None) -> Self: ...
    @classmethod
    def from_private_key(cls, file_obj: _HasReadlines, password: str | None = None) -> Self: ...
    def write_private_key_file(
        self, filename: StrOrBytesPath, password: str | None = None, file_format: FileFormat = PEM  # noqa: Y011
    ) -> None: ...
    def write_private_key(
        self, file_obj: SupportsWrite[str], password: str | None = None, file_format: FileFormat = PEM  # noqa: Y011
    ) -> None: ...
    def load_certificate(self, value: Message | str) -> None: ...

class PublicBlob:
    """
    OpenSSH plain public key or OpenSSH signed public key (certificate).

    Tries to be as dumb as possible and barely cares about specific
    per-key-type data.

    .. note::

        Most of the time you'll want to call `from_file`, `from_string` or
        `from_message` for useful instantiation, the main constructor is
        basically "I should be using ``attrs`` for this."
    """
    key_type: str
    key_blob: bytes
    comment: str
    def __init__(self, type_: str, blob: bytes, comment: str | None = None) -> None:
        """
        Create a new public blob of given type and contents.

        :param str type_: Type indicator, eg ``ssh-rsa``.
        :param bytes blob: The blob bytes themselves.
        :param str comment: A comment, if one was given (e.g. file-based.)
        """
        ...
    @classmethod
    def from_file(cls, filename: StrOrBytesPath) -> Self: ...
    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a public blob from a ``-cert.pub``-style string."""
        ...
    @classmethod
    def from_message(cls, message: Message) -> Self:
        """
        Create a public blob from a network `.Message`.

        Specifically, a cert-bearing pubkey auth packet, because by definition
        OpenSSH-style certificates 'are' their own network representation."
        """
        ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
