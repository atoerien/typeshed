"""Small, fast HTTP client library for Python."""

import builtins
import email.message
import http.client
import re
from _ssl import _PasswordType
from _typeshed import ConvertibleToFloat, ConvertibleToInt, Incomplete, MaybeNone, StrOrBytesPath
from collections.abc import Generator
from ssl import _SSLMethod
from typing import Any, ClassVar, Final, Literal, TypeVar, overload
from typing_extensions import Self

from .error import *

_T = TypeVar("_T", default=str)
_R = TypeVar("_R")
_D = TypeVar("_D")

__author__: Final[str]
__copyright__: Final[str]
__contributors__: Final[list[str]]
__license__: Final[str]
__version__: Final[str]
__all__ = [
    "debuglevel",
    "FailedToDecompressContent",
    "Http",
    "HttpLib2Error",
    "ProxyInfo",
    "RedirectLimit",
    "RedirectMissingLocation",
    "Response",
    "RETRIES",
    "UnimplementedDigestAuthOptionError",
    "UnimplementedHmacDigestAuthOptionError",
]

def has_timeout(timeout: float | None) -> bool: ...

debuglevel: Final[int]
RETRIES: Final[int]
DEFAULT_MAX_REDIRECTS: Final[int]
HOP_BY_HOP: Final[list[str]]
SAFE_METHODS: Final[tuple[str, ...]]
REDIRECT_CODES: Final[frozenset[int]]
CA_CERTS: Final[str]
DEFAULT_TLS_VERSION: Final[_SSLMethod]
URI: Final[re.Pattern[str]]

def parse_uri(uri: str) -> tuple[str | MaybeNone, str | MaybeNone, str | MaybeNone, str | MaybeNone, str | MaybeNone]:
    """
    Parses a URI using the regex given in Appendix B of RFC 3986.

    (scheme, authority, path, query, fragment) = parse_uri(uri)
    """
    ...
def urlnorm(uri: str) -> tuple[str | MaybeNone, str | MaybeNone, str | MaybeNone, str | MaybeNone]: ...

re_url_scheme: Final[re.Pattern[str]]
re_unsafe: Final[re.Pattern[str]]

def safename(filename: str | bytes) -> str:
    """
    Return a filename suitable for the cache.
    Strips dangerous and common characters to create a filename we
    can use to store the cache in.
    """
    ...

NORMALIZE_SPACE: Final[re.Pattern[str]]
USE_WWW_AUTH_STRICT_PARSING: Final[int]

class Authentication:
    path: Incomplete
    host: Incomplete
    credentials: Incomplete
    http: Incomplete
    def __init__(self, credentials, host, request_uri: str, headers, response, content, http) -> None: ...
    def depth(self, request_uri: str) -> int: ...
    def inscope(self, host: str, request_uri: str) -> bool: ...
    def request(self, method, request_uri, headers, content) -> None:
        """
        Modify the request headers to add the appropriate
        Authorization header. Over-rise this in sub-classes.
        """
        ...
    def response(self, response, content) -> bool:
        """
        Gives us a chance to update with new nonces
        or such returned from the last authorized response.
        Over-rise this in sub-classes if necessary.

        Return TRUE is the request is to be retried, for
        example Digest may return stale=true.
        """
        ...
    def __eq__(self, auth: object) -> bool: ...
    def __ne__(self, auth: object) -> bool: ...
    def __lt__(self, auth: object) -> bool: ...
    def __gt__(self, auth: object) -> bool: ...
    def __le__(self, auth: object) -> bool: ...
    def __ge__(self, auth: object) -> bool: ...
    def __bool__(self) -> bool: ...

class BasicAuthentication(Authentication):
    def __init__(self, credentials, host, request_uri, headers, response, content, http) -> None: ...
    def request(self, method, request_uri, headers, content) -> None:
        """
        Modify the request headers to add the appropriate
        Authorization header.
        """
        ...

class DigestAuthentication(Authentication):
    """
    Only do qop='auth' and MD5, since that
    is all Apache currently implements
    """
    challenge: Incomplete
    A1: Incomplete
    def __init__(self, credentials, host, request_uri, headers, response, content, http) -> None: ...
    def request(self, method, request_uri, headers, content, cnonce=None):
        """Modify the request headers"""
        ...
    def response(self, response, content) -> bool: ...

class HmacDigestAuthentication(Authentication):
    """Adapted from Robert Sayre's code and DigestAuthentication above."""
    challenge: Incomplete
    hashmod: Incomplete
    pwhashmod: Incomplete
    key: Incomplete
    __author__: ClassVar[str]
    def __init__(self, credentials, host, request_uri, headers, response, content, http) -> None: ...
    def request(self, method, request_uri, headers, content) -> None:
        """Modify the request headers"""
        ...
    def response(self, response, content) -> bool: ...

class WsseAuthentication(Authentication):
    """
    This is thinly tested and should not be relied upon.
    At this time there isn't any third party server to test against.
    Blogger and TypePad implemented this algorithm at one point
    but Blogger has since switched to Basic over HTTPS and
    TypePad has implemented it wrong, by never issuing a 401
    challenge but instead requiring your client to telepathically know that
    their endpoint is expecting WSSE profile="UsernameToken".
    """
    def __init__(self, credentials, host, request_uri, headers, response, content, http) -> None: ...
    def request(self, method, request_uri, headers, content) -> None:
        """
        Modify the request headers to add the appropriate
        Authorization header.
        """
        ...

class GoogleLoginAuthentication(Authentication):
    Auth: str
    def __init__(self, credentials, host, request_uri, headers, response, content, http) -> None: ...
    def request(self, method, request_uri, headers, content) -> None:
        """
        Modify the request headers to add the appropriate
        Authorization header.
        """
        ...

class FileCache:
    """
    Uses a local directory as a store for cached files.
    Not really safe to use if multiple threads or processes are going to
    be running on the same cache.
    """
    cache: Incomplete
    safe: Incomplete
    def __init__(self, cache, safe=...) -> None: ...
    def get(self, key): ...
    def set(self, key, value) -> None: ...
    def delete(self, key) -> None: ...

class Credentials:
    credentials: Incomplete
    def __init__(self) -> None: ...
    def add(self, name, password, domain: str = "") -> None: ...
    def clear(self) -> None: ...
    def iter(self, domain) -> Generator[tuple[str, str]]: ...

class KeyCerts(Credentials):
    """
    Identical to Credentials except that
    name/password are mapped to key/cert.
    """
    def add(self, key, cert, domain, password) -> None: ...  # type: ignore[override]
    def iter(self, domain) -> Generator[tuple[str, str, str]]: ...  # type: ignore[override]

class AllHosts: ...

class ProxyInfo:
    """Collect information required to use a proxy."""
    bypass_hosts: Incomplete
    def __init__(
        self, proxy_type, proxy_host, proxy_port, proxy_rdns: bool = True, proxy_user=None, proxy_pass=None, proxy_headers=None
    ) -> None:
        """
        Args:

        proxy_type: The type of proxy server.  This must be set to one of
        socks.PROXY_TYPE_XXX constants.  For example:  p =
        ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP, proxy_host='localhost',
        proxy_port=8000)
        proxy_host: The hostname or IP address of the proxy server.
        proxy_port: The port that the proxy server is running on.
        proxy_rdns: If True (default), DNS queries will not be performed
        locally, and instead, handed to the proxy to resolve.  This is useful
        if the network does not allow resolution of non-local names. In
        httplib2 0.9 and earlier, this defaulted to False.
        proxy_user: The username used to authenticate with the proxy server.
        proxy_pass: The password used to authenticate with the proxy server.
        proxy_headers: Additional or modified headers for the proxy connect
        request.
        """
        ...
    def astuple(self): ...
    def isgood(self): ...
    def applies_to(self, hostname): ...
    def bypass_host(self, hostname):
        """Has this host been excluded from the proxy config"""
        ...

def proxy_info_from_environment(method: Literal["http", "https"] = "http") -> ProxyInfo | None:
    """
    Read proxy info from the environment variables.
    
    """
    ...
def proxy_info_from_url(url: str, method: Literal["http", "https"] = "http", noproxy: str | None = None) -> ProxyInfo:
    """
    Construct a ProxyInfo from a URL (such as http_proxy env var)
    
    """
    ...

class HTTPConnectionWithTimeout(http.client.HTTPConnection):
    """
    HTTPConnection subclass that supports timeouts

    HTTPConnection subclass that supports timeouts

    All timeouts are in seconds. If None is passed for timeout then
    Python's default timeout for sockets will be used. See for example
    the docs of socket.setdefaulttimeout():
    http://docs.python.org/library/socket.html#socket.setdefaulttimeout
    """
    proxy_info: Incomplete
    def __init__(self, host, port=None, timeout=None, proxy_info=None) -> None: ...
    sock: Incomplete
    def connect(self) -> None:
        """Connect to the host and port specified in __init__."""
        ...

class HTTPSConnectionWithTimeout(http.client.HTTPSConnection):
    """
    This class allows communication via SSL.

    All timeouts are in seconds. If None is passed for timeout then
    Python's default timeout for sockets will be used. See for example
    the docs of socket.setdefaulttimeout():
    http://docs.python.org/library/socket.html#socket.setdefaulttimeout
    """
    disable_ssl_certificate_validation: bool
    ca_certs: StrOrBytesPath | None
    proxy_info: Incomplete
    key_file: StrOrBytesPath | None
    cert_file: StrOrBytesPath | None
    key_password: _PasswordType | None
    def __init__(
        self,
        host: str,
        port: int | None = None,
        key_file: StrOrBytesPath | None = None,
        cert_file: StrOrBytesPath | None = None,
        timeout: float | None = None,
        proxy_info=None,
        ca_certs: StrOrBytesPath | None = None,
        disable_ssl_certificate_validation: bool = False,
        tls_maximum_version=None,
        tls_minimum_version=None,
        key_password: _PasswordType | None = None,
    ) -> None: ...
    sock: Incomplete
    def connect(self) -> None:
        """Connect to a host on a given (SSL) port."""
        ...

SCHEME_TO_CONNECTION: Final[dict[Literal["http", "https"], type[http.client.HTTPConnection]]]

class Http:
    """
    An HTTP client that handles:

    - all methods
    - caching
    - ETags
    - compression,
    - HTTPS
    - Basic
    - Digest
    - WSSE

    and more.
    """
    proxy_info: Incomplete
    ca_certs: Incomplete
    disable_ssl_certificate_validation: bool
    tls_maximum_version: Incomplete
    tls_minimum_version: Incomplete
    connections: Incomplete
    cache: FileCache
    credentials: Credentials
    certificates: KeyCerts
    authorizations: list[Authentication]
    follow_redirects: bool
    redirect_codes: frozenset[int]
    optimistic_concurrency_methods: list[str]
    safe_methods: list[str]
    follow_all_redirects: bool
    ignore_etag: bool
    force_exception_to_status_code: bool
    timeout: float | None
    forward_authorization_headers: bool
    limit_kwargs: dict[str, float]
    def __init__(
        self,
        cache: str | FileCache | None = None,
        timeout: float | None = None,
        proxy_info=...,
        ca_certs=None,
        disable_ssl_certificate_validation: bool = False,
        tls_maximum_version=None,
        tls_minimum_version=None,
        decode_limit_hard: ConvertibleToInt | None = None,
        decode_limit_safe: ConvertibleToInt | None = None,
        decode_limit_ratio: ConvertibleToFloat | None = None,
        decode_limit_chunk: ConvertibleToInt | None = None,
    ) -> None: ...
    def close(self) -> None: ...
    def add_credentials(self, name, password, domain: str = "") -> None: ...
    def add_certificate(self, key, cert, domain, password=None) -> None: ...
    def clear_credentials(self) -> None: ...
    def request(self, uri, method: str = "GET", body=None, headers=None, redirections=5, connection_type=None): ...

class Response(dict[str, str | _T]):
    """An object more like email.message than httplib.HTTPResponse."""
    fromcache: bool
    version: int
    status: int
    reason: str
    previous: Response[_T] | None
    def __init__(self, info: http.client.HTTPResponse | email.message.Message | builtins.dict[str, _T]) -> None: ...
    @property
    def dict(self) -> Self: ...

@overload
def try_value_or_env(
    to: type[_R], value: Any, env_key: str, default: None = None  # `value` type depends on what `to()` can convert
) -> _R | None: ...
@overload
def try_value_or_env(
    to: type[_R], value: Any, env_key: str, default: _D = ...  # `value` type depends on what `to()` can convert
) -> _R | _D: ...
