"""
pygments.regexopt
~~~~~~~~~~~~~~~~~

An algorithm that generates optimized regexes for matching long lists of
literal strings.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

import re
from collections.abc import Iterable, Sequence
from operator import itemgetter
from typing import Final

CS_ESCAPE: Final[re.Pattern[str]]
FIRST_ELEMENT: Final[itemgetter[int]]

def commonprefix(m: Iterable[str]) -> str:
    """Given an iterable of strings, returns the longest common leading substring"""
    ...
def make_charset(letters: Iterable[str]) -> str: ...
def regex_opt_inner(strings: Sequence[str], open_paren: str) -> str:
    """Return a regex that matches any string in the sorted list of strings."""
    ...
def regex_opt(strings: Iterable[str], prefix: str = "", suffix: str = "") -> str:
    """
    Return a compiled regex that matches any string in the given list.

    The strings to match must be literal strings, not regexes.  They will be
    regex-escaped.

    *prefix* and *suffix* are pre- and appended to the final regex.
    """
    ...
