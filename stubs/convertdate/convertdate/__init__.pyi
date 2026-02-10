"""
The Convertdate library contains methods and functions for converting dates between
different calendar systems.

It was originally developed as as `Python Date Util <(http://sourceforge.net/projects/pythondateutil/>`__
by Phil Schwartz. It has been significantly updated and expanded.

Most of the original code is ported from
`Fourmilab's calendar converter <http://www.fourmilab.ch/documents/calendar/>`__,
which was developed by John Walker.

The algorithms are believed to be derived from: Meeus, Jean. `Astronomical Algorithms`,
Richmond: Willmann-Bell, 1991 (ISBN 0-943396-35-2)
"""

from typing import Final

from . import (
    armenian as armenian,
    bahai as bahai,
    coptic as coptic,
    daycount as daycount,
    dublin as dublin,
    french_republican as french_republican,
    gregorian as gregorian,
    hebrew as hebrew,
    holidays as holidays,
    indian_civil as indian_civil,
    islamic as islamic,
    iso as iso,
    julian as julian,
    julianday as julianday,
    mayan as mayan,
    ordinal as ordinal,
    persian as persian,
    positivist as positivist,
    utils as utils,
)

__version__: Final[str]

__all__ = [
    "armenian",
    "bahai",
    "coptic",
    "daycount",
    "dublin",
    "french_republican",
    "gregorian",
    "hebrew",
    "holidays",
    "indian_civil",
    "islamic",
    "iso",
    "julian",
    "julianday",
    "mayan",
    "ordinal",
    "persian",
    "positivist",
    "utils",
]
