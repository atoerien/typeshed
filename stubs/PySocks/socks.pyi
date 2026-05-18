import logging
import socket
import types
from _typeshed import ReadableBuffer
from collections.abc import Callable, Iterable, Mapping
from typing import Final, ParamSpec, TypeAlias, TypeVar, overload

__version__: Final[str]

log: logging.Logger  # undocumented

_ProxyType: TypeAlias = int

PROXY_TYPE_SOCKS4: Final[_ProxyType]
SOCKS4: Final[_ProxyType]
PROXY_TYPE_SOCKS5: Final[_ProxyType]
SOCKS5: Final[_ProxyType]
PROXY_TYPE_HTTP: Final[_ProxyType]
HTTP: Final[_ProxyType]

PROXY_TYPES: Final[dict[str, _ProxyType]]
PRINTABLE_PROXY_TYPES: Final[dict[_ProxyType, str]]

_T = TypeVar("_T")
_P = ParamSpec("_P")

def set_self_blocking(function: Callable[_P, _T]) -> Callable[_P, _T]: ...  # undocumented

class ProxyError(IOError):
    """Socket_err contains original socket.error exception."""
    msg: str
    socket_err: socket.error
    def __init__(self, msg: str, socket_err: socket.error | None = None) -> None: ...

class GeneralProxyError(ProxyError): ...
class ProxyConnectionError(ProxyError): ...
class SOCKS5AuthError(ProxyError): ...
class SOCKS5Error(ProxyError): ...
class SOCKS4Error(ProxyError): ...
class HTTPError(ProxyError): ...

SOCKS4_ERRORS: Final[Mapping[int, str]]
SOCKS5_ERRORS: Final[Mapping[int, str]]
DEFAULT_PORTS: Final[Mapping[_ProxyType, int]]

_DefaultProxy: TypeAlias = tuple[_ProxyType | None, str | None, int | None, bool, bytes | None, bytes | None]

def set_default_proxy(
    proxy_type: _ProxyType | None = None,
    addr: str | None = None,
    port: int | None = None,
    rdns: bool = True,
    username: str | None = None,
    password: str | None = None,
) -> None:
    """
    Sets a default proxy.

    All further socksocket objects will use the default unless explicitly
    changed. All parameters are as for socket.set_proxy().
    """
    ...
def setdefaultproxy(
    proxy_type: _ProxyType | None = None,
    addr: str | None = None,
    port: int | None = None,
    rdns: bool = True,
    username: str | None = None,
    password: str | None = None,
    *,
    proxytype: _ProxyType = ...,
) -> None: ...
def get_default_proxy() -> _DefaultProxy | None:
    """Returns the default proxy, set by set_default_proxy."""
    ...

getdefaultproxy = get_default_proxy

def wrap_module(module: types.ModuleType) -> None:
    """
    Attempts to replace a module's socket library with a SOCKS socket.

    Must set a default proxy using set_default_proxy(...) first. This will
    only work on modules that import socket directly into the namespace;
    most of the Python Standard Library falls into this category.
    """
    ...

wrapmodule = wrap_module

_Endpoint: TypeAlias = tuple[str, int]

def create_connection(
    dest_pair: _Endpoint,
    timeout: int | None = None,
    source_address: _Endpoint | None = None,
    proxy_type: _ProxyType | None = None,
    proxy_addr: str | None = None,
    proxy_port: int | None = None,
    proxy_rdns: bool = True,
    proxy_username: str | None = None,
    proxy_password: str | None = None,
    socket_options: (
        Iterable[tuple[int, int, int | ReadableBuffer] | tuple[int, int, None, int]] | None
    ) = None,  # values passing to `socket.setsockopt` method
) -> socksocket:
    """
    create_connection(dest_pair, *[, timeout], **proxy_args) -> socket object

    Like socket.create_connection(), but connects to proxy
    before returning the socket object.

    dest_pair - 2-tuple of (IP/hostname, port).
    **proxy_args - Same args passed to socksocket.set_proxy() if present.
    timeout - Optional socket timeout value, in seconds.
    source_address - tuple (host, port) for the socket to bind to as its source
    address before connecting (only for compatibility)
    """
    ...

class _BaseSocket(socket.socket):  # undocumented
    """Allows Python 2 delegated methods such as send() to be overridden."""
    ...

class socksocket(_BaseSocket):
    """
    socksocket([family[, type[, proto]]]) -> socket object

    Open a SOCKS enabled socket. The parameters are the same as
    those of the standard socket init. In order for SOCKS to work,
    you must specify family=AF_INET and proto=0.
    The "type" argument must be either SOCK_STREAM or SOCK_DGRAM.
    """
    default_proxy: _DefaultProxy | None  # undocumented
    proxy: _DefaultProxy  # undocumented
    proxy_sockname: _Endpoint | None  # undocumented
    proxy_peername: _Endpoint | None  # undocumented
    def __init__(
        self, family: socket.AddressFamily = ..., type: socket.SocketKind = ..., proto: int = 0, fileno: int | None = None
    ) -> None: ...
    def settimeout(self, timeout: float | None) -> None: ...
    def gettimeout(self) -> float | None: ...
    def setblocking(self, v: bool) -> None: ...
    def set_proxy(
        self,
        proxy_type: _ProxyType | None = None,
        addr: str | None = None,
        port: int | None = None,
        rdns: bool = True,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """
        Sets the proxy to be used.

        proxy_type -  The type of the proxy to be used. Three types
                        are supported: PROXY_TYPE_SOCKS4 (including socks4a),
                        PROXY_TYPE_SOCKS5 and PROXY_TYPE_HTTP
        addr -        The address of the server (IP or DNS).
        port -        The port of the server. Defaults to 1080 for SOCKS
                        servers and 8080 for HTTP proxy servers.
        rdns -        Should DNS queries be performed on the remote side
                       (rather than the local side). The default is True.
                       Note: This has no effect with SOCKS4 servers.
        username -    Username to authenticate with to the server.
                       The default is no authentication.
        password -    Password to authenticate with to the server.
                       Only relevant when username is also provided.
        """
        ...
    def setproxy(
        self,
        proxy_type: _ProxyType | None = None,
        addr: str | None = None,
        port: int | None = None,
        rdns: bool = True,
        username: str | None = None,
        password: str | None = None,
        *,
        proxytype: _ProxyType = ...,
    ) -> None: ...
    def bind(self, address: socket._Address, /) -> None: ...

    @overload
    def sendto(self, bytes: ReadableBuffer, address: socket._Address) -> int: ...
    @overload
    def sendto(self, bytes: ReadableBuffer, flags: int, address: socket._Address) -> int: ...

    def send(self, bytes: ReadableBuffer, flags: int = 0) -> int: ...
    def recvfrom(self, bufsize: int, flags: int = 0) -> tuple[bytes, _Endpoint]: ...
    def recv(self, bufsize: int, flags: int = 0) -> bytes: ...
    def close(self) -> None: ...
    def get_proxy_sockname(self) -> _Endpoint | None:
        """Returns the bound IP address and port number at the proxy."""
        ...
    getproxysockname = get_proxy_sockname
    def get_proxy_peername(self) -> _Endpoint | None:
        """Returns the IP and port number of the proxy."""
        ...
    getproxypeername = get_proxy_peername
    def get_peername(self) -> _Endpoint | None:
        """
        Returns the IP address and port number of the destination machine.

        Note: get_proxy_peername returns the proxy.
        """
        ...
    getpeername = get_peername
    @set_self_blocking
    def connect(self, dest_pair: _Endpoint, catch_errors: bool | None = None) -> None:
        """
        Connects to the specified destination through a proxy.
        Uses the same API as socket's connect().
        To select the proxy server, use set_proxy().

        dest_pair - 2-tuple of (IP/hostname, port).
        """
        ...
    @set_self_blocking
    def connect_ex(self, dest_pair: _Endpoint) -> int:
        """
        https://docs.python.org/3/library/socket.html#socket.socket.connect_ex
        Like connect(address), but return an error indicator instead of raising an exception for errors returned by the C-level connect() call (other problems, such as "host not found" can still raise exceptions).
        """
        ...
