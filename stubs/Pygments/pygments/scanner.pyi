"""
pygments.scanner
~~~~~~~~~~~~~~~~

This library implements a regex based scanner. Some languages
like Pascal are easy to parse but have some keywords that
depend on the context. Because of this it's impossible to lex
that just by using a regular expression lexer like the
`RegexLexer`.

Have a look at the `DelphiLexer` to get an idea of how to use
this scanner.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from re import Match, Pattern, RegexFlag

class EndOfText(RuntimeError):
    """
    Raise if end of text is reached and the user
    tried to call a match function.
    """
    ...

class Scanner:
    """
    Simple scanner

    All method patterns are regular expression strings (not
    compiled expressions!)
    """
    data: str
    data_length: int
    start_pos: int
    pos: int
    flags: int | RegexFlag
    last: str | None
    match: str | None
    def __init__(self, text: str, flags: int | RegexFlag = 0) -> None:
        """
        :param text:    The text which should be scanned
        :param flags:   default regular expression flags
        """
        ...
    @property
    def eos(self) -> bool:
        """`True` if the scanner reached the end of text."""
        ...
    def check(self, pattern: str | Pattern[str]) -> Match[str] | None:
        """
        Apply `pattern` on the current position and return
        the match object. (Doesn't touch pos). Use this for
        lookahead.
        """
        ...
    def test(self, pattern: str | Pattern[str]) -> bool:
        """
        Apply a pattern on the current position and check
        if it patches. Doesn't touch pos.
        """
        ...
    def scan(self, pattern: str | Pattern[str]) -> bool:
        """
        Scan the text for the given pattern and update pos/match
        and related fields. The return value is a boolean that
        indicates if the pattern matched. The matched value is
        stored on the instance as ``match``, the last value is
        stored as ``last``. ``start_pos`` is the position of the
        pointer before the pattern was matched, ``pos`` is the
        end position.
        """
        ...
    def get_char(self) -> None:
        """Scan exactly one char."""
        ...
