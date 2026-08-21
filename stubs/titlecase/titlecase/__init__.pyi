"""
Original Perl version by: John Gruber http://daringfireball.net/ 10 May 2008
Python version by Stuart Colville http://muffinresearch.co.uk
License: http://www.opensource.org/licenses/mit-license.php
"""

import logging
import re
from typing import Final, Protocol, TypeAlias, overload, type_check_only
from typing_extensions import LiteralString

import regex

_Pattern: TypeAlias = re.Pattern[str] | regex.Pattern[str]

__all__ = ["titlecase"]
__version__: Final[str]
logger: Final[logging.Logger]

REGEX_AVAILABLE: Final[bool]

SMALL: Final[str]
PUNCT: Final[str]

SMALL_WORDS: _Pattern
SMALL_FIRST: _Pattern
SMALL_LAST: _Pattern
SUBPHRASE: _Pattern

MAC_MC: Final[_Pattern]
MR_MRS_MS_DR: Final[_Pattern]
INLINE_PERIOD: Final[_Pattern]
UC_ELSEWHERE: Final[_Pattern]
CAPFIRST: Final[_Pattern]
APOS_SECOND: Final[_Pattern]
UC_INITIALS: Final[_Pattern]

@type_check_only
class _CallbackProtocol(Protocol):
    def __call__(self, word: str, /, *, all_caps: bool) -> str | None: ...

class Immutable: ...
class ImmutableString(str, Immutable): ...
class ImmutableBytes(bytes, Immutable): ...

@overload
def set_small_word_list() -> None: ...
@overload
def set_small_word_list(small: str) -> None: ...

def titlecase(
    text: str, callback: _CallbackProtocol | None = None, small_first_last: bool = True, preserve_blank_lines: bool = False
) -> LiteralString:
    """
    :param text: Titlecases input text
    :param callback: Callback function that returns the titlecase version of a specific word
    :param small_first_last: Capitalize small words (e.g. 'A') at the beginning; disabled when recursing
    :type text: str
    :type callback: function
    :type small_first_last: bool

    This filter changes all words to Title Caps, and attempts to be clever
    about *un*capitalizing SMALL words like a/an/the in the input.

    The list of "SMALL words" which are not capped comes from
    the New York Times Manual of Style, plus 'vs' and 'v'.
    """
    ...
def create_wordlist_filter_from_file(file_path: str | None) -> _CallbackProtocol:
    """
    Load a list of abbreviations from the file with the provided path,
    reading one abbreviation from each line, and return a callback to
    be passed to the `titlecase` function for preserving their given
    canonical capitalization during title-casing.
    """
    ...
def cmd() -> None:
    """Handler for command line invocation"""
    ...
