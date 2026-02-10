"""
The Mayan calendar was developed in Mesoamerica. It includes two interlocking
cycles: the 260-day _Tzolkin_ cycle and the 365-day _Haab'_ cycle. In the _Tzolkin_ cycle,
each day is numbered 1-13 and has one of 20 day names. The _Haab'_ cycle comprises 18 months
of 20 days, along with five additional days (_Wayebʼ_).

The calendrical system also includes the
`Long Count <https://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar>`__,
a modified base-20 counting scheme. Dates in the long count are usually written in the form *7.18.14.8.12*.
"""

from _typeshed import Unused
from collections.abc import Generator
from typing import Final, Literal, NoReturn, overload

EPOCH: Final = 584282.5
HAAB: Final[list[str]]
HAAB_TRANSLATIONS: Final[list[str]]
TZOLKIN: Final[list[str]]
TZOLKIN_TRANSLATIONS: Final[list[str]]

def to_jd(baktun: int, katun: int, tun: int, uinal: int, kin: int) -> float:
    """Determine Julian day from Mayan long count"""
    ...
def from_jd(jd: float) -> tuple[int, int, int, int, int]:
    """Calculate Mayan long count from Julian day"""
    ...
def to_gregorian(baktun: int, katun: int, tun: int, uinal: int, kin: int) -> tuple[int, int, int]: ...
def from_gregorian(year: int, month: int, day: int) -> tuple[int, int, int, int, int]: ...
def to_haab(jd: float) -> tuple[int, str]:
    """Determine Mayan Haab "month" and day from Julian day"""
    ...
def to_tzolkin(jd: float) -> tuple[int, str]:
    """Determine Mayan Tzolkin "month" and day from Julian day"""
    ...
def lc_to_haab(baktun: int, katun: int, tun: int, uinal: int, kin: int) -> tuple[int, str]: ...
def lc_to_tzolkin(baktun: int, katun: int, tun: int, uinal: int, kin: int) -> tuple[int, str]: ...
def lc_to_haab_tzolkin(baktun: int, katun: int, tun: int, uinal: int, kin: int) -> str: ...
def translate_haab(h: str) -> str | None: ...
def translate_tzolkin(tz: str) -> str | None: ...
def tzolkin_generator(number: int | None = None, name: str | None = None) -> Generator[tuple[int, str]]:
    """
    For a given tzolkin name/number combination, return a generator
    that gives cycle, starting with the input
    """
    ...
def longcount_generator(
    baktun: int, katun: int, tun: int, uinal: int, kin: int
) -> Generator[tuple[int, int, int, int, int], None, NoReturn]:
    """Generate long counts, starting with input"""
    ...
def next_haab(month: str, jd: float) -> float:
    """For a given haab month and a julian day count, find the next start of that month on or after the JDC"""
    ...
def next_tzolkin(tzolkin: tuple[int, str], jd: float) -> float:
    """For a given tzolk'in day, and a julian day count, find the next occurrance of that tzolk'in after the date"""
    ...
def next_tzolkin_haab(tzolkin: tuple[int, str], haab: tuple[int, str], jd: float) -> float:
    """
    Find the next occurence of a haab-tzolk'in combination.

    Requires a Julian day count as the starting place for the search.
    """
    ...
def month_length(month: str) -> Literal[5, 20]:
    """Not the actual length of the month, but accounts for the 5 unlucky/nameless days"""
    ...
@overload
def haab_monthcalendar(
    baktun: int, katun: int, tun: int, uinal: int, kin: int, jdc: None = None
) -> list[list[tuple[int | None, tuple[int, str] | None, tuple[int, int, int, int, int] | None]]]:
    """For a given long count, return a calender of the current haab month, divided into tzolkin "weeks\""""
    ...
@overload
def haab_monthcalendar(
    baktun: Unused = None, katun: Unused = None, tun: Unused = None, uinal: Unused = None, kin: Unused = None, jdc: float = ...
) -> list[list[tuple[int | None, tuple[int, str] | None, tuple[int, int, int, int, int] | None]]]:
    """For a given long count, return a calender of the current haab month, divided into tzolkin "weeks\""""
    ...
def haab_monthcalendar_prospective(
    haabmonth: str, jdc: float
) -> list[list[tuple[int | None, tuple[int, str] | None, tuple[int, int, int, int, int] | None]]]:
    """Give the monthcalendar for the next occurance of given haab month after jdc"""
    ...
