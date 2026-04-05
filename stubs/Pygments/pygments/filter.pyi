"""
pygments.filter
~~~~~~~~~~~~~~~

Module that implements the default filter.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from collections.abc import Iterable, Iterator

from pygments.lexer import Lexer
from pygments.token import _TokenType

def apply_filters(stream, filters, lexer=None):
    """
    Use this method to apply an iterable of filters to
    a stream. If lexer is given it's forwarded to the
    filter, otherwise the filter receives `None`.
    """
    ...
def simplefilter(f):
    """
    Decorator that converts a function into a filter::

        @simplefilter
        def lowercase(self, lexer, stream, options):
            for ttype, value in stream:
                yield ttype, value.lower()
    """
    ...

class Filter:
    """
    Default filter. Subclass this class or use the `simplefilter`
    decorator to create own filters.
    """
    options: Incomplete
    def __init__(self, **options) -> None: ...
    def filter(self, lexer: Lexer, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class FunctionFilter(Filter):
    """
    Abstract class used by `simplefilter` to create simple
    function filters on the fly. The `simplefilter` decorator
    automatically creates subclasses of this class for
    functions passed to it.
    """
    function: Incomplete
    def __init__(self, **options) -> None: ...
    def filter(self, lexer: Lexer, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...
