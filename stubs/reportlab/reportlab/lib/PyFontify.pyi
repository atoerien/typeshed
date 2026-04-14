"""
Module to analyze Python source code; for syntax coloring tools.

Interface::

    tags = fontify(pytext, searchfrom, searchto)

 - The 'pytext' argument is a string containing Python source code.
 - The (optional) arguments 'searchfrom' and 'searchto' may contain a slice in pytext.
 - The returned value is a list of tuples, formatted like this::
    [('keyword', 0, 6, None), ('keyword', 11, 17, None), ('comment', 23, 53, None), etc. ]

 - The tuple contents are always like this::
    (tag, startindex, endindex, sublist)

 - tag is one of 'keyword', 'string', 'comment' or 'identifier'
 - sublist is not used, hence always None.
"""

import re
from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

def replace(src, sep, rep): ...

keywordsList: list[str]
commentPat: str
pat: str
quotePat: str
tripleQuotePat: str
nonKeyPat: str
keyPat: str
matchPat: str
matchRE: re.Pattern[str]
idKeyPat: str
idRE: re.Pattern[str]

def fontify(pytext, searchfrom: int = 0, searchto=None) -> list[tuple[str, int, int, Incomplete]]: ...
def test(path) -> None: ...
