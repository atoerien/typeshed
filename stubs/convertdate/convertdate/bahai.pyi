"""
The Bahá'í (Badí) calendar is a solar calendar with 19 months of 19 days.

An intercalary period, Ayyam-i-Há, occurs between the 18th and 19th months, has
either four or five days. Dates in this period are returned as month 19, and
the month of ‘Alá is always reported as month 20.

.. code-block:: python

   from convertdate import bahai
   # the first day of Ayyam-i-Ha:
   bahai.to_gregorian(175, 19, 1)
   # (2019, 2, 26)
   # The first day of 'Ala:
   bahai.to_gregorian(175, 20, 1)
   # (2019, 3, 2)
"""

from typing import Final

EPOCH: Final = 2394646.5
EPOCH_GREGORIAN_YEAR: Final = 1844
TEHRAN: Final = 51.4215, 35.6944
WEEKDAYS: Final = ("Jamál", "Kamál", "Fidál", "Idál", "Istijlál", "Istiqlál", "Jalál")
MONTHS: Final[tuple[str, ...]]
ENGLISH_MONTHS: Final[tuple[str, ...]]
BAHA: Final = 1
JALAL: Final = 2
JAMAL: Final = 3
AZAMAT: Final = 4
NUR: Final = 5
RAHMAT: Final = 6
KALIMAT: Final = 7
KAMAL: Final = 8
ASMA: Final = 9
IZZAT: Final = 10
MASHIYYAT: Final = 11
ILM: Final = 12
QUDRAT: Final = 13
QAWL: Final = 14
MASAIL: Final = 15
SHARAF: Final = 16
SULTAN: Final = 17
MULK: Final = 18
AYYAMIHA: Final = 19
ALA: Final = 20

def gregorian_nawruz(year: int) -> tuple[int, int]:
    """
    Return Nawruz in the Gregorian calendar.
    Returns a tuple (month, day), where month is always 3
    """
    ...
def to_jd(year: int, month: int, day: int) -> float:
    """Determine Julian day from Bahai date"""
    ...
def from_jd(jd: float) -> tuple[int, int, int]:
    """Calculate Bahai date from Julian day"""
    ...
def from_gregorian(year: int, month: int, day: int) -> tuple[int, int, int]: ...
def to_gregorian(year: int, month: int, day: int) -> tuple[int, int, int]: ...
def month_length(year: int, month: int) -> int: ...
def monthcalendar(year: int, month: int) -> list[list[int | None]]: ...
def format(year: int, month: int, day: int, lang: str | None = None) -> str:
    """Convert a Baha'i date into a string with the format DD MONTH YYYY."""
    ...
