"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""

import sys
from _typeshed import Incomplete, StrOrBytesPath
from collections.abc import Generator, Iterable, Mapping
from contextlib import _GeneratorContextManager
from io import BufferedWriter
from typing import AnyStr
from typing_extensions import TypeAlias

from . import compat, cookies, exceptions, structures
from .models import PreparedRequest, Request

_Uri: TypeAlias = str | bytes
OrderedDict = compat.OrderedDict
cookiejar_from_dict = cookies.cookiejar_from_dict
CaseInsensitiveDict = structures.CaseInsensitiveDict
InvalidURL = exceptions.InvalidURL

NETRC_FILES: tuple[str, str]
DEFAULT_CA_BUNDLE_PATH: Incomplete
DEFAULT_PORTS: dict[str, int]
DEFAULT_ACCEPT_ENCODING: str

def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    ...
def super_len(o): ...
def get_netrc_auth(url: _Uri, raise_errors: bool = False) -> tuple[str, str] | None: ...
def guess_filename(obj): ...
def extract_zipped_paths(path): ...
def atomic_open(filename: StrOrBytesPath) -> _GeneratorContextManager[BufferedWriter]: ...
def from_key_val_list(value): ...
def to_key_val_list(value): ...
def parse_list_header(value): ...
def parse_dict_header(value): ...
def unquote_header_value(value, is_filename: bool = False): ...
def dict_from_cookiejar(cj): ...
def add_dict_to_cookiejar(cj, cookie_dict): ...
def get_encodings_from_content(content): ...
def get_encoding_from_headers(headers: Mapping[str, str]) -> str | None: ...
def stream_decode_response_unicode(iterator, r): ...
def iter_slices(string: str, slice_length: int | None) -> Generator[str]: ...
def get_unicode_from_response(r): ...

UNRESERVED_SET: frozenset[str]

def unquote_unreserved(uri: str) -> str:
    """
    Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded.

    :rtype: str
    """
    ...
def requote_uri(uri: str) -> str:
    """
    Re-quote the given URI.

    This function passes the given URI through an unquote/quote cycle to
    ensure that it is fully and consistently quoted.

    :rtype: str
    """
    ...
def address_in_network(ip: str, net: str) -> bool:
    """
    This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """
    ...
def dotted_netmask(mask: int) -> str:
    """
    Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """
    ...
def is_ipv4_address(string_ip: str) -> bool:
    """:rtype: bool"""
    ...
def is_valid_cidr(string_network: str) -> bool:
    """
    Very simple check of the cidr format in no_proxy variable.

    :rtype: bool
    """
    ...
def set_environ(env_name: str, value: None) -> _GeneratorContextManager[None]:
    """
    Set the environment variable 'env_name' to 'value'

    Save previous value, yield, and then restore the previous value stored in
    the environment variable 'env_name'.

    If 'value' is None, do nothing
    """
    ...
def should_bypass_proxies(url: _Uri, no_proxy: Iterable[str] | None) -> bool:
    """
    Returns whether we should bypass proxies or not.

    :rtype: bool
    """
    ...
def get_environ_proxies(url: _Uri, no_proxy: Iterable[str] | None = None) -> dict[Incomplete, Incomplete]:
    """
    Return a dict of environment proxies.

    :rtype: dict
    """
    ...
def select_proxy(url: _Uri, proxies: Mapping[str, str] | None) -> str:
    """
    Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """
    ...
def resolve_proxies(
    request: Request | PreparedRequest, proxies: dict[str, str] | None, trust_env: bool = True
) -> dict[str, str]:
    """
    This method takes proxy information from a request and configuration
    input to resolve a mapping of target proxies. This will consider settings
    such as NO_PROXY to strip proxy configurations.

    :param request: Request or PreparedRequest
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    :param trust_env: Boolean declaring whether to trust environment configs

    :rtype: dict
    """
    ...
def default_user_agent(name: str = "python-requests") -> str:
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    ...
def default_headers() -> CaseInsensitiveDict[str]:
    """:rtype: requests.structures.CaseInsensitiveDict"""
    ...
def parse_header_links(value: str) -> list[dict[str, str]]:
    """
    Return a list of parsed link headers proxies.

    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"

    :rtype: list
    """
    ...
def guess_json_utf(data):
    """:rtype: str"""
    ...
def prepend_scheme_if_needed(url, new_scheme):
    """
    Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """
    ...
def get_auth_from_url(url: _Uri) -> tuple[str, str]:
    """
    Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    ...
def to_native_string(string, encoding="ascii"):
    """
    Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    ...
def urldefragauth(url: _Uri):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """
    ...
def rewind_body(prepared_request: PreparedRequest) -> None:
    """
    Move file pointer back to its recorded starting position
    so it can be read again on redirect.
    """
    ...
def check_header_validity(header: tuple[AnyStr, AnyStr]) -> None:
    """
    Verifies that header parts don't contain leading whitespace
    reserved characters, or return characters.

    :param header: tuple, in the format (name, value).
    """
    ...

if sys.platform == "win32":
    def proxy_bypass_registry(host: str) -> bool: ...
    def proxy_bypass(host: str) -> bool: ...
