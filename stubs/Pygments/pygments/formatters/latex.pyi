from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable
from typing import TypeVar

from pygments.formatter import Formatter
from pygments.lexer import Lexer
from pygments.token import _TokenType

_T = TypeVar("_T", str, bytes)

__all__ = ["LatexFormatter"]

class LatexFormatter(Formatter[_T]):
    docclass: Incomplete
    preamble: Incomplete
    linenos: Incomplete
    linenostart: Incomplete
    linenostep: Incomplete
    verboptions: Incomplete
    nobackground: Incomplete
    commandprefix: Incomplete
    texcomments: Incomplete
    mathescape: Incomplete
    escapeinside: Incomplete
    left: Incomplete
    right: Incomplete
    envname: Incomplete
    def get_style_defs(self, arg: str = ""): ...
    def format_unencoded(self, tokensource: Iterable[tuple[_TokenType, str]], outfile: SupportsWrite[str]) -> None: ...

class LatexEmbeddedLexer(Lexer):
    """
    This lexer takes one lexer as argument, the lexer for the language
    being formatted, and the left and right delimiters for escaped text.

    First everything is scanned using the language lexer to obtain
    strings and comments. All other consecutive tokens are merged and
    the resulting text is scanned for escaped segments, which are given
    the Token.Escape type. Finally text that is not escaped is scanned
    again with the language lexer.
    """
    left: Incomplete
    right: Incomplete
    lang: Incomplete
    def __init__(self, left, right, lang, **options) -> None: ...
    def get_tokens_unprocessed(self, text): ...
