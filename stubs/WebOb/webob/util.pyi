from collections.abc import Callable
from typing import AnyStr

def html_escape(s: object) -> str:
    """
    HTML-escape a string or object

    This converts any non-string objects passed into it to strings
    (actually, using ``unicode()``).  All values returned are
    non-unicode strings (using ``&#num;`` entities for all non-ASCII
    characters).

    None is treated specially, and returns the empty string.
    """
    ...
def urljoin(base: str, url: str | None) -> str:
    """
    Resolve a URI reference relative to a base URI (RFC 3986 section 5).

    A replacement for ``urllib.parse.urljoin()``. The standard library
    implementation follows the WHATWG URL living standard (on Python
    3.10+) by removing ASCII tab, CR, and LF anywhere in the URL and
    stripping leading and trailing C0 control and space characters
    before parsing. Those transformations can silently turn an otherwise
    harmless relative reference such as ``" //evil.example"`` into a
    protocol-relative or absolute URL, which has repeatedly led to open
    redirect issues when normalizing the ``Location`` header (see
    CVE-2024-42353/GHSA-mg3v-6m49-jhp3, GHSA-fh3h-vg37-cc95, and
    GHSA-6hx8-3wjj-gr8g).

    This implementation resolves the reference exactly as given,
    character for character, with no whitespace removal whatsoever.
    """
    ...
def header_docstring(header: str, rfc_section: str) -> str: ...
def warn_deprecation(text: str, version: str, stacklevel: int) -> None: ...

status_reasons: dict[int, str]
status_generic_reasons: dict[int, str]

def strings_differ(string1: AnyStr, string2: AnyStr, compare_digest: Callable[[AnyStr, AnyStr], bool] = ...) -> bool:
    """
    Check whether two strings differ while avoiding timing attacks.

    This function returns True if the given strings differ and False
    if they are equal.  It's careful not to leak information about *where*
    they differ as a result of its running time, which can be very important
    to avoid certain timing-related crypto attacks:

        http://seb.dbzteam.org/crypto/python-oauth-timing-hmac.pdf

    .. versionchanged:: 1.5
       Support :func:`hmac.compare_digest` if it is available (Python 2.7.7+
       and Python 3.3+).
    """
    ...
