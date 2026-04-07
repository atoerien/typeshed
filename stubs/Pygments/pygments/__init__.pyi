"""
Pygments
~~~~~~~~

Pygments is a syntax highlighting package written in Python.

It is a generic syntax highlighter for general use in all kinds of software
such as forum systems, wikis or other applications that need to prettify
source code. Highlights are:

* a wide range of common languages and markup formats is supported
* special attention is paid to details, increasing quality by a fair amount
* support for new languages and formats are added easily
* a number of output formats, presently HTML, LaTeX, RTF, SVG, all image
  formats that PIL supports, and ANSI sequences
* it is usable as a command-line tool and as a library
* ... and it highlights even Brainfuck!

The `Pygments master branch`_ is installable with ``easy_install Pygments==dev``.

.. _Pygments master branch:
   https://github.com/pygments/pygments/archive/master.zip#egg=Pygments-dev

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import SupportsWrite
from collections.abc import Iterable, Iterator
from typing import Final, TypeVar, overload

from pygments.formatter import Formatter
from pygments.lexer import Lexer
from pygments.token import _TokenType

_T = TypeVar("_T", str, bytes)

__version__: Final[str]
__docformat__: Final = "restructuredtext"
__all__ = ["lex", "format", "highlight"]

def lex(code: str, lexer: Lexer) -> Iterator[tuple[_TokenType, str]]:
    """
    Lex `code` with the `lexer` (must be a `Lexer` instance)
    and return an iterable of tokens. Currently, this only calls
    `lexer.get_tokens()`.
    """
    ...
@overload
def format(tokens: Iterable[tuple[_TokenType, str]], formatter: Formatter[_T], outfile: SupportsWrite[_T]) -> None: ...
@overload
def format(tokens: Iterable[tuple[_TokenType, str]], formatter: Formatter[_T], outfile: None = None) -> _T: ...
@overload
def highlight(code: str, lexer: Lexer, formatter: Formatter[_T], outfile: SupportsWrite[_T]) -> None: ...
@overload
def highlight(code: str, lexer: Lexer, formatter: Formatter[_T], outfile: None = None) -> _T: ...
