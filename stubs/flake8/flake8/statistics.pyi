"""Statistic collection logic for Flake8."""

from collections.abc import Generator
from typing import NamedTuple

from .violation import Violation

class Statistics:
    def __init__(self) -> None: ...
    def error_codes(self) -> list[str]: ...
    def record(self, error: Violation) -> None: ...
    def statistics_for(self, prefix: str, filename: str | None = None) -> Generator[Statistic]: ...

class Key(NamedTuple):
    """
    Simple key structure for the Statistics dictionary.

    To make things clearer, easier to read, and more understandable, we use a
    namedtuple here for all Keys in the underlying dictionary for the
    Statistics object.
    """
    filename: str
    code: str
    @classmethod
    def create_from(cls, error: Violation) -> Key:
        """Create a Key from :class:`flake8.violation.Violation`."""
        ...
    def matches(self, prefix: str, filename: str | None) -> bool:
        """
        Determine if this key matches some constraints.

        :param prefix:
            The error code prefix that this key's error code should start with.
        :param filename:
            The filename that we potentially want to match on. This can be
            None to only match on error prefix.
        :returns:
            True if the Key's code starts with the prefix and either filename
            is None, or the Key's filename matches the value passed in.
        """
        ...

class Statistic:
    """
    Simple wrapper around the logic of each statistic.

    Instead of maintaining a simple but potentially hard to reason about
    tuple, we create a class which has attributes and a couple
    convenience methods on it.
    """
    error_code: str
    filename: str
    message: str
    count: int
    def __init__(self, error_code: str, filename: str, message: str, count: int) -> None:
        """Initialize our Statistic."""
        ...
    @classmethod
    def create_from(cls, error: Violation) -> Statistic:
        """Create a Statistic from a :class:`flake8.violation.Violation`."""
        ...
    def increment(self) -> None:
        """Increment the number of times we've seen this error in this file."""
        ...
