"""
Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
"""

import sys
from collections.abc import Iterable
from os import PathLike
from typing import AnyStr

__all__ = ["filter", "fnmatch", "fnmatchcase", "translate"]
if sys.version_info >= (3, 14):
    __all__ += ["filterfalse"]

def fnmatch(name: AnyStr | PathLike[AnyStr], pat: AnyStr | PathLike[AnyStr]) -> bool: ...
def fnmatchcase(name: AnyStr, pat: AnyStr) -> bool: ...
def filter(names: Iterable[AnyStr | PathLike[AnyStr]], pat: AnyStr | PathLike[AnyStr]) -> list[AnyStr]: ...
def translate(pat: str) -> str: ...

if sys.version_info >= (3, 14):
    def filterfalse(names: Iterable[AnyStr | PathLike[AnyStr]], pat: AnyStr | PathLike[AnyStr]) -> list[AnyStr]: ...
