import datetime
from typing import Any, TypeAlias

from ..core import Calendar

_HebrewDate: TypeAlias = Any | datetime.date  # from `pyluach.dates` package

class Israel(Calendar):
    """Israel"""
    def get_hebrew_independence_day(self, jewish_year: int) -> list[tuple[_HebrewDate, str]]:
        """
        Returns the independence day eve and independence day dates
        according to the given hebrew year

        :param jewish_year: the specific hebrew year for calculating
                            the independence day dates
        :return: independence day dates
                 in the type of List[Tuple[HebrewDate, str]]
        """
        ...
