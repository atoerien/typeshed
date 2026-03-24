"""
oauthlib.utils
~~~~~~~~~~~~~~

This module contains utility methods used by various parts of the OAuth
spec.
"""

from collections.abc import Callable, Iterable
from typing import Final, TypeVar

_T = TypeVar("_T")

UNICODE_ASCII_CHARACTER_SET: Final[str]

def filter_params(
    target: Callable[[dict[str, object] | Iterable[tuple[str, object]], _T], object],
) -> Callable[[list[str], _T], object]: ...
def filter_oauth_params(
    params: dict[str, object] | Iterable[tuple[str, object]],
) -> list[str]: ...  # we don't care about second (object) part
def escape(u: str) -> str: ...
def unescape(u: str) -> str: ...
def parse_keqv_list(l: list[str]) -> dict[str, str]:
    """A unicode-safe version of urllib2.parse_keqv_list"""
    ...
def parse_http_list(u: str) -> list[str]:
    """A unicode-safe version of urllib2.parse_http_list"""
    ...
def parse_authorization_header(authorization_header: str) -> list[tuple[str, str]]:
    """Parse an OAuth authorization header into a list of 2-tuples"""
    ...
