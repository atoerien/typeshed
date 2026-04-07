"""
pygments.filters
~~~~~~~~~~~~~~~~

Module containing filter lookup functions and default
filters.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import ConvertibleToInt
from collections.abc import Callable, Generator, Iterable, Iterator
from re import Pattern
from typing import Any, ClassVar, Final, Literal

from pygments.filter import Filter
from pygments.lexer import Lexer
from pygments.token import _TokenType

def find_filter_class(filtername: str) -> type[Filter] | None:
    """Lookup a filter by name. Return None if not found."""
    ...

# Keyword arguments are forwarded to the filter class.
def get_filter_by_name(filtername: str, **options: Any) -> Filter:
    """
    Return an instantiated filter.

    Options are passed to the filter initializer if wanted.
    Raise a ClassNotFound if not found.
    """
    ...
def get_all_filters() -> Generator[str]:
    """Return a generator of all filter names."""
    ...

class CodeTagFilter(Filter):
    """
    Highlight special code tags in comments and docstrings.

    Options accepted:

    `codetags` : list of strings
       A list of strings that are flagged as code tags.  The default is to
       highlight ``XXX``, ``TODO``, ``FIXME``, ``BUG`` and ``NOTE``.

    .. versionchanged:: 2.13
       Now recognizes ``FIXME`` by default.
    """
    tag_re: Pattern[str]
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(
        self, *, codetags: str | list[str] | tuple[str, ...] = ["XXX", "TODO", "FIXME", "BUG", "NOTE"], **options: Any
    ) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class SymbolFilter(Filter):
    r"""
    Convert mathematical symbols into Unicode characters.

    Examples are ``\<longrightarrow>`` in Isabelle or
    ``\longrightarrow`` in LaTeX.

    This is mostly useful for HTML or console output when you want to
    approximate the source rendering you'd see in an IDE.

    Options accepted:

    `lang` : string
       The symbol language. Must be one of ``'isabelle'`` or
       ``'latex'``.  The default is ``'isabelle'``.
    """
    latex_symbols: ClassVar[dict[str, str]]
    isabelle_symbols: ClassVar[dict[str, str]]
    lang_map: ClassVar[dict[Literal["isabelle", "latex"], dict[str, str]]]
    symbols: dict[str, str]  # One of latex_symbols or isabelle_symbols.
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(self, *, lang: Literal["isabelle", "latex"] = "isabelle", **options: Any) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class KeywordCaseFilter(Filter):
    """
    Convert keywords to lowercase or uppercase or capitalize them.

    This means first letter uppercase, rest lowercase.

    This can be useful e.g. if you highlight Pascal code and want to adapt the
    code to your styleguide.

    Options accepted:

    `case` : string
       The casing to convert keywords to. Must be one of ``'lower'``,
       ``'upper'`` or ``'capitalize'``.  The default is ``'lower'``.
    """
    convert: Callable[[str], str]
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(self, *, case: Literal["lower", "upper", "capitalize"] = "lower", **options: Any) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class NameHighlightFilter(Filter):
    """
    Highlight a normal Name (and Name.*) token with a different token type.

    Example::

        filter = NameHighlightFilter(
            names=['foo', 'bar', 'baz'],
            tokentype=Name.Function,
        )

    This would highlight the names "foo", "bar" and "baz"
    as functions. `Name.Function` is the default token type.

    Options accepted:

    `names` : list of strings
      A list of names that should be given the different token type.
      There is no default.
    `tokentype` : TokenType or string
      A token type or a string containing a token type name that is
      used for highlighting the strings in `names`.  The default is
      `Name.Function`.
    """
    names: set[str]
    tokentype: _TokenType
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(
        self, *, names: str | list[str] | tuple[str, ...] = [], tokentype: str | _TokenType | None = None, **options: Any
    ) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class ErrorToken(Exception): ...

class RaiseOnErrorTokenFilter(Filter):
    """
    Raise an exception when the lexer generates an error token.

    Options accepted:

    `excclass` : Exception class
      The exception class to raise.
      The default is `pygments.filters.ErrorToken`.

    .. versionadded:: 0.8
    """
    exception: type[Exception]
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(self, *, excclass: type[Exception] = ..., **options: Any) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class VisibleWhitespaceFilter(Filter):
    """
    Convert tabs, newlines and/or spaces to visible characters.

    Options accepted:

    `spaces` : string or bool
      If this is a one-character string, spaces will be replaces by this string.
      If it is another true value, spaces will be replaced by ``·`` (unicode
      MIDDLE DOT).  If it is a false value, spaces will not be replaced.  The
      default is ``False``.
    `tabs` : string or bool
      The same as for `spaces`, but the default replacement character is ``»``
      (unicode RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK).  The default value
      is ``False``.  Note: this will not work if the `tabsize` option for the
      lexer is nonzero, as tabs will already have been expanded then.
    `tabsize` : int
      If tabs are to be replaced by this filter (see the `tabs` option), this
      is the total number of characters that a tab should be expanded to.
      The default is ``8``.
    `newlines` : string or bool
      The same as for `spaces`, but the default replacement character is ``¶``
      (unicode PILCROW SIGN).  The default value is ``False``.
    `wstokentype` : bool
      If true, give whitespace the special `Whitespace` token type.  This allows
      styling the visible whitespace differently (e.g. greyed out), but it can
      disrupt background colors.  The default is ``True``.

    .. versionadded:: 0.8
    """
    spaces: str
    tabs: str
    newlines: str
    wstt: bool
    def __init__(
        self,
        *,
        spaces: str | bool = False,
        tabs: str | bool = False,
        newlines: str | bool = False,
        tabsize: ConvertibleToInt = 8,
        wstokentype: bool | int | str = True,  # Any value accepted by get_bool_opt.
        # Arbitrary additional keyword arguments are permitted and are stored in self.options.
        **options: Any,
    ) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class GobbleFilter(Filter):
    """
    Gobble source code lines (eats initial characters).

    This filter drops the first ``n`` characters off every line of code.  This
    may be useful when the source code fed to the lexer is indented by a fixed
    amount of space that isn't desired in the output.

    Options accepted:

    `n` : int
       The number of characters to gobble.

    .. versionadded:: 1.2
    """
    n: int
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(self, *, n: ConvertibleToInt = 0, **options: Any) -> None: ...
    def gobble(self, value: str, left: int) -> tuple[str, int]: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

class TokenMergeFilter(Filter):
    """
    Merge consecutive tokens with the same token type in the output stream.

    .. versionadded:: 1.2
    """
    # Arbitrary additional keyword arguments are permitted and are stored in self.options.
    def __init__(self, **options: Any) -> None: ...
    def filter(self, lexer: Lexer | None, stream: Iterable[tuple[_TokenType, str]]) -> Iterator[tuple[_TokenType, str]]: ...

FILTERS: Final[dict[str, type[Filter]]]
