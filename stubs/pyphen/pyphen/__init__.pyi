"""
Pyphen
======

Pure Python module to hyphenate text, inspired by Ruby's Text::Hyphen.
"""

from collections.abc import Generator
from pathlib import Path
from typing import SupportsInt, TypeAlias
from typing_extensions import Self

__all__ = ("LANGUAGES", "Pyphen", "language_fallback")
LANGUAGES: dict[str, Path]
_Data: TypeAlias = tuple[str, int, int]

def language_fallback(language: str) -> str:
    """
    Get a fallback language available in our dictionaries.

    http://www.unicode.org/reports/tr35/#Locale_Inheritance

    We use the normal truncation inheritance. This function needs aliases
    including scripts for languages with multiple regions available.
    """
    ...

class AlternativeParser:
    """
    Parser of nonstandard hyphen pattern alternative.

    The instance returns a special int with data about the current position in
    the pattern when called with an odd value.
    """
    change: str
    index: int
    cut: int

    def __init__(self, pattern: str, alternative: str) -> None: ...
    def __call__(self, value: str | SupportsInt) -> int: ...

class DataInt(int):
    """``int`` with some other data can be stuck to in a ``data`` attribute."""
    data: _Data | None

    def __new__(cls, value: int, data: _Data | None = ..., reference: DataInt | None = ...) -> Self:
        """
        Create a new ``DataInt``.

        Call with ``reference=dataint_object`` to use the data from another
        ``DataInt``.
        """
        ...

class HyphDict:
    """Hyphenation patterns."""
    patterns: dict[str, tuple[int, tuple[int, ...]]]
    cache: dict[str, list[DataInt]]
    maxlen: int

    def __init__(self, path: Path) -> None:
        """
        Read a ``hyph_*.dic`` and parse its patterns.

        :param path: Path of hyph_*.dic to read
        """
        ...
    def positions(self, word: str) -> list[DataInt]:
        """
        Get a list of positions where the word can be hyphenated.

        :param word: unicode string of the word to hyphenate

        E.g. for the dutch word 'lettergrepen' this method returns ``[3, 6,
        9]``.

        Each position is a ``DataInt`` with a data attribute.

        If the data attribute is not ``None``, it contains a tuple with
        information about nonstandard hyphenation at that point: ``(change,
        index, cut)``.

        change
          a string like ``'ff=f'``, that describes how hyphenation should
          take place.

        index
          where to substitute the change, counting from the current point

        cut
          how many characters to remove while substituting the nonstandard
          hyphenation
        """
        ...

class Pyphen:
    """Hyphenation class, with methods to hyphenate strings in various ways."""
    hd: HyphDict

    def __init__(
        self, filename: str | Path | None = ..., lang: str | None = ..., left: int = 2, right: int = 2, cache: bool = True
    ) -> None:
        """
        Create an hyphenation instance for given lang or filename.

        :param filename: filename or Path of hyph_*.dic to read
        :param lang: lang of the included dict to use if no filename is given
        :param left: minimum number of characters of the first syllabe
        :param right: minimum number of characters of the last syllabe
        :param cache: if ``True``, use cached copy of the hyphenation patterns
        """
        ...
    def positions(self, word: str) -> list[DataInt]:
        """
        Get a list of positions where the word can be hyphenated.

        :param word: unicode string of the word to hyphenate

        See also ``HyphDict.positions``. The points that are too far to the
        left or right are removed.
        """
        ...
    def iterate(self, word: str) -> Generator[tuple[str, str]]:
        """
        Iterate over all hyphenation possibilities, the longest first.

        :param word: unicode string of the word to hyphenate
        """
        ...
    def wrap(self, word: str, width: int, hyphen: str = "-") -> tuple[str, str] | None:
        """
        Get the longest possible first part and the last part of a word.

        :param word: unicode string of the word to hyphenate
        :param width: maximum length of the first part
        :param hyphen: unicode string used as hyphen character

        The first part has the hyphen already attached.

        Returns ``None`` if there is no hyphenation point before ``width``, or
        if the word could not be hyphenated.
        """
        ...
    def inserted(self, word: str, hyphen: str = "-") -> str:
        """
        Get the word as a string with all the possible hyphens inserted.

        :param word: unicode string of the word to hyphenate
        :param hyphen: unicode string used as hyphen character

        E.g. for the dutch word ``'lettergrepen'``, this method returns the
        unicode string ``'let-ter-gre-pen'``. The hyphen string to use can be
        given as the second parameter, that defaults to ``'-'``.
        """
        ...
    __call__ = iterate
