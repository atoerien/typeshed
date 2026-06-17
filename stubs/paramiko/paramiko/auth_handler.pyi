"""`.AuthHandler`"""

from collections.abc import Callable
from threading import Event
from typing import TypeAlias

from paramiko.message import Message
from paramiko.pkey import PKey
from paramiko.transport import Transport

_InteractiveCallback: TypeAlias = Callable[[str, str, list[tuple[str, bool]]], list[str]]

class AuthHandler:
    """Internal class to handle the mechanics of authentication."""
    transport: Transport
    username: str | None
    authenticated: bool
    auth_event: Event | None
    auth_method: str
    banner: str | None
    password: str | None
    private_key: PKey | None
    interactive_handler: _InteractiveCallback | None
    submethods: str | None
    auth_username: str | None
    auth_fail_count: int
    gss_host: str | None
    gss_deleg_creds: bool
    def __init__(self, transport: Transport) -> None: ...
    def is_authenticated(self) -> bool: ...
    def get_username(self) -> str | None: ...
    def auth_none(self, username: str, event: Event) -> None: ...
    def auth_publickey(self, username: str, key: PKey, event: Event) -> None: ...
    def auth_password(self, username: str, password: str, event: Event) -> None: ...
    def auth_interactive(self, username: str, handler: _InteractiveCallback, event: Event, submethods: str = "") -> None: ...
    def abort(self) -> None: ...
    def wait_for_response(self, event: Event) -> list[str]: ...

class AuthOnlyHandler(AuthHandler):
    """
    AuthHandler, and just auth, no service requests!

    .. versionadded:: 3.2
    """
    def send_auth_request(
        self, username: str, method: str, finish_message: Callable[[Message], None] | None = None
    ) -> list[str]:
        """
        Submit a userauth request message & wait for response.

        Performs the transport message send call, sets self.auth_event, and
        will lock-n-block as necessary to both send, and wait for response to,
        the USERAUTH_REQUEST.

        Most callers will want to supply a callback to ``finish_message``,
        which accepts a Message ``m`` and may call mutator methods on it to add
        more fields.
        """
        ...
    def auth_none(self, username: str) -> list[str]: ...  # type: ignore[override]
    def auth_publickey(self, username: str, key: PKey) -> list[str]: ...  # type: ignore[override]
    def auth_password(self, username: str, password: str) -> list[str]: ...  # type: ignore[override]
    def auth_interactive(self, username: str, handler: _InteractiveCallback, submethods: str = "") -> list[str]:
        """response_list = handler(title, instructions, prompt_list)"""
        ...
