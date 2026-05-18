"""
This module contains practical examples of Docutils client code.

Importing this module from client code is not recommended; its contents are
subject to change in future Docutils releases.  Instead, it is recommended
that you copy and paste the parts you need into your own code, modifying as
necessary.
"""

from _typeshed import Incomplete, StrPath
from typing import Literal, TypeAlias, overload

from docutils.core import Publisher
from docutils.nodes import document
from docutils.writers import _WriterParts

_HTMLHeaderLevel: TypeAlias = Literal[1, 2, 3, 4, 5, 6]

def html_parts(
    input_string: str | bytes,
    source_path: StrPath | None = None,
    destination_path: StrPath | None = None,
    input_encoding: str = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> _WriterParts: ...

@overload
def html_body(
    input_string: str | bytes,
    source_path: StrPath | None = None,
    destination_path: StrPath | None = None,
    input_encoding: str = "unicode",
    output_encoding: Literal["unicode"] = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> str:
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    ...
@overload
def html_body(
    input_string: str | bytes,
    source_path: StrPath | None = None,
    destination_path: StrPath | None = None,
    input_encoding: str = "unicode",
    output_encoding: str = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> str | bytes: ...

def internals(
    source: str,
    source_path: StrPath | None = None,
    input_encoding: str = "unicode",
    settings_overrides: dict[str, Incomplete] | None = None,
) -> tuple[document | None, Publisher]:
    """
    Return the document tree and publisher, for exploring Docutils internals.

    Parameters: see `html_parts()`.
    """
    ...
