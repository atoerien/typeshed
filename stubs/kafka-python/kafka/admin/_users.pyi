"""
User management mixin for KafkaAdminClient.

Also defines ScramMechanism, UserCredentialDeletion,
and UserCredentialUpsertion data classes.
"""

from _typeshed import ReadableBuffer
from collections.abc import Sequence
from enum import IntEnum
from typing import Final

class UserAdminMixin:
    """Mixin providing user management methods for KafkaAdminClient."""
    def alter_user_scram_credentials(self, alterations: Sequence[UserScramCredentialDeletion | UserScramCredentialUpsertion]):
        """
        Alter SCRAM credentials for one or more users.

        Arguments:
            alterations: A list of UserScramCredentialDeletion and/or
                UserScramCredentialUpsertion objects describing the
                credentials to delete and/or insert/update.

        Returns:
            A dict mapping user name -> error message (or None on success).
        """
        ...
    def describe_user_scram_credentials(self, users: Sequence[str] | None = None):
        """
        Describe SCRAM credentials for one or more users.

        Arguments:
            users (list of str, optional): User names to describe. If None,
                describe all users with SCRAM credentials.

        Returns:
            A dict mapping user name to a dict with keys
            ``'error'`` (None or error message) and ``'credential_infos'``
            (list of {'mechanism': ScramMechanism, 'iterations': int}).
        """
        ...

class ScramMechanism(IntEnum):
    """An enumeration."""
    UNKNOWN = 0
    SCRAM_SHA_256 = 1
    SCRAM_SHA_512 = 2
    @property
    def hash_name(self) -> str: ...

class UserScramCredentialDeletion:
    """
    Specifies that a SCRAM credential should be deleted.

    Arguments:
        user (str): The user name.
        mechanism (ScramMechanism or int or str): The SCRAM mechanism to
            delete for this user.
    """
    user: str
    mechanism: ScramMechanism
    def __init__(self, user: str, mechanism: ScramMechanism | int | str) -> None: ...

class UserScramCredentialUpsertion:
    """
    Specifies that a SCRAM credential should be inserted or updated.

    Arguments:
        user (str): The user name.
        mechanism (ScramMechanism or int or str): The SCRAM mechanism.
        password (bytes or str): The plaintext password. The salted
            password sent to the broker is derived via PBKDF2-HMAC using
            the given salt and iteration count.

    Keyword Arguments:
        iterations (int, optional): PBKDF2 iteration count. Default: 4096.
        salt (bytes, optional): Salt to use. If omitted, a random 24-byte
            salt is generated.
    """
    DEFAULT_ITERATIONS: Final = 4096
    user: str
    mechanism: ScramMechanism
    iterations: int
    salt: ReadableBuffer
    salted_password: bytes
    def __init__(
        self,
        user: str,
        mechanism: ScramMechanism | int | str,
        password: str | ReadableBuffer,
        iterations: int | None = None,
        salt: ReadableBuffer | None = None,
    ) -> None: ...
