"""
The `ordinal date <https://en.wikipedia.org/wiki/Ordinal_date>` specifies the day
of year as a number between 1 and 366.

Ordinal dates are represented by a tuple: ``(year, dayofyear)``
"""

def to_jd(year: int, dayofyear: int) -> float:
    """Return Julian day count of given ordinal date."""
    ...
def from_jd(jd: float) -> tuple[int, int]:
    """
    Convert a Julian day count to an ordinal date.

    The day of year is derived from the Gregorian date rather than the raw
    ``jd``. Both ``to_jd`` values carry the same half-day offset, so their
    difference is an exact whole number of days; subtracting ``jd`` directly
    leaves a ``.5`` remainder that ``round`` pushes the wrong way (e.g.
    ``365.5`` -> ``366``), reporting a non-existent day 366 in common years.
    """
    ...
def from_gregorian(year: int, month: int, day: int) -> tuple[int, int]:
    """Convert a Gregorian date to an ordinal date."""
    ...
def to_gregorian(year: int, dayofyear: int) -> tuple[int, int, int]:
    """Convert an ordinal date to a Gregorian date."""
    ...
