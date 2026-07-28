from _typeshed import Incomplete, StrPath, SupportsRead, SupportsWrite
from collections.abc import Callable, Generator, Iterable
from enum import Enum
from typing import Final, Generic, NamedTuple, TypeVar

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

_T = TypeVar("_T")

__all__ = ["read_gml", "parse_gml", "generate_gml", "write_gml"]

def escape(text):
    """
    Use XML character references to escape characters.

    Use XML character references for unprintable or non-ASCII
    characters, double quotes and ampersands in a string
    """
    ...
def unescape(text):
    """Replace XML character references with the referenced characters"""
    ...
def literal_destringizer(rep: str):
    """
    Convert a Python literal to the value it represents.

    Parameters
    ----------
    rep : string
        A Python literal.

    Returns
    -------
    value : object
        The value of the Python literal.

    Raises
    ------
    ValueError
        If `rep` is not a Python literal.
    """
    ...
@_dispatchable
def read_gml(
    path: StrPath | SupportsRead[bytes], label: str = "label", destringizer: Callable[..., Incomplete] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def parse_gml(
    lines: str | Iterable[str], label: str = "label", destringizer: Callable[..., Incomplete] | None = None
) -> Graph[Incomplete]: ...

class Pattern(Enum):
    """encodes the index of each token-matching pattern in `tokenize`."""
    KEYS = 0
    REALS = 1
    INTS = 2
    STRINGS = 3
    DICT_START = 4
    DICT_END = 5
    COMMENT_WHITESPACE = 6

class Token(NamedTuple, Generic[_T]):
    """Token(category, value, line, position)"""
    category: Pattern
    value: _T
    line: int
    position: int

LIST_START_VALUE: Final = "_networkx_list_start"

def parse_gml_lines(lines, label, destringizer): ...
def literal_stringizer(value) -> str: ...
def generate_gml(G: Graph[_Node], stringizer: Callable[..., Incomplete] | None = None) -> Generator[Incomplete, Incomplete]: ...
def write_gml(
    G: Graph[_Node], path: StrPath | SupportsWrite[bytes], stringizer: Callable[..., Incomplete] | None = None
) -> None: ...
