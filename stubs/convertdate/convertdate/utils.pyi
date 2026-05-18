"""Helper utilities useful in several converters."""

from typing import Final, Literal, overload

TROPICALYEAR: Final[float]

@overload
def amod(a: float, b: int) -> int:
    """Modulus function which returns numerator if modulus is zero"""
    ...
@overload
def amod(a: float, b: float) -> float: ...

def jwday(j: float) -> int: ...

@overload
def weekday_before(weekday: int, jd: int) -> int: ...
@overload
def weekday_before(weekday: int, jd: float) -> float: ...

@overload
def search_weekday(weekday: int, jd: int, direction: Literal[-1, 1], offset: int) -> int:
    """
    Determine the Julian date for the next or previous weekday

    Arguments:
        weekday (int): Day of week desired, 0 = Monday
        jd (float): Julian date to begin search
        direction(int): 1 = next weekday, -1 = last weekday
        offset(int): Offset from jd to begin search.
    """
    ...
@overload
def search_weekday(weekday: int, jd: float, direction: Literal[-1, 1], offset: int) -> float: ...

@overload
def nearest_weekday(weekday: int, jd: int) -> int: ...
@overload
def nearest_weekday(weekday: int, jd: float) -> float: ...

@overload
def next_weekday(weekday: int, jd: int) -> int: ...
@overload
def next_weekday(weekday: int, jd: float) -> float: ...

@overload
def next_or_current_weekday(weekday: int, jd: int) -> int: ...
@overload
def next_or_current_weekday(weekday: int, jd: float) -> float: ...

@overload
def previous_weekday(weekday: int, jd: int) -> int: ...
@overload
def previous_weekday(weekday: int, jd: float) -> float: ...

@overload
def previous_or_current_weekday(weekday: int, jd: int) -> int: ...
@overload
def previous_or_current_weekday(weekday: int, jd: float) -> float: ...

@overload
def n_weeks(weekday: int, jd: int, nthweek: int) -> int: ...
@overload
def n_weeks(weekday: int, jd: float, nthweek: int) -> float: ...

def monthcalendarhelper(start_weekday: int, month_length: int) -> list[list[int | None]]: ...
def nth_day_of_month(n: int, weekday: int, month: int, year: int) -> tuple[int, int, int]:
    """
    Return (year, month, day) tuple that represents nth weekday of month in year.
    If n==0, returns last weekday of month. Weekdays: Monday=0
    """
    ...
