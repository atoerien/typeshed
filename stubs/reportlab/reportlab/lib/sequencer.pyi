"""A Sequencer class counts things. It aids numbering and formatting lists."""

from collections.abc import Callable

__all__ = ["Sequencer", "getSequencer", "setSequencer"]

from typing import overload

class _Counter:
    """
    Private class used by Sequencer.  Each counter
    knows its format, and the IDs of anything it
    resets, as well as its value. Starts at zero
    and increments just before you get the new value,
    so that it is still 'Chapter 5' and not 'Chapter 6'
    when you print 'Figure 5.1'
    """
    _value: int
    def __init__(self) -> None: ...
    def setFormatter(self, formatFunc: Callable[[int], str]) -> None: ...
    def reset(self, value: int | None = None) -> None: ...
    def next(self) -> int: ...
    __next__ = next
    def _this(self) -> int: ...
    def nextf(self) -> str:
        """Returns next value formatted"""
        ...
    def thisf(self) -> str: ...
    def chain(self, otherCounter: _Counter) -> None: ...

class Sequencer:
    """
    Something to make it easy to number paragraphs, sections,
    images and anything else.  The features include registering
    new string formats for sequences, and 'chains' whereby
    some counters are reset when their parents.
    It keeps track of a number of
    'counters', which are created on request:
    Usage::

        >>> seq = layout.Sequencer()
        >>> seq.next('Bullets')
        1
        >>> seq.next('Bullets')
        2
        >>> seq.next('Bullets')
        3
        >>> seq.reset('Bullets')
        >>> seq.next('Bullets')
        1
        >>> seq.next('Figures')
        1
        >>>
    """
    def __init__(self) -> None: ...
    def __next__(self) -> int:
        """
        Retrieves the numeric value for the given counter, then
        increments it by one.  New counters start at one.
        """
        ...
    def next(self, counter=None) -> int: ...
    def thisf(self, counter=None) -> str: ...
    def nextf(self, counter=None) -> str:
        """
        Retrieves the numeric value for the given counter, then
        increments it by one.  New counters start at one.
        """
        ...
    def setDefaultCounter(self, default=None) -> None:
        """Changes the key used for the default"""
        ...
    def registerFormat(self, format: str, func: Callable[[int], str]) -> None:
        """
        Registers a new formatting function.  The funtion
        must take a number as argument and return a string;
        fmt is a short menmonic string used to access it.
        """
        ...
    def setFormat(self, counter, format: str) -> None:
        """
        Specifies that the given counter should use
        the given format henceforth.
        """
        ...
    def reset(self, counter=None, base: int = 0) -> None: ...
    def chain(self, parent, child) -> None: ...
    def __getitem__(self, key: str) -> str:
        """
        Allows compact notation to support the format function.
        s['key'] gets current value, s['key+'] increments.
        """
        ...
    def format(self, template: str) -> str:
        """The crowning jewels - formats multi-level lists."""
        ...
    def dump(self) -> None:
        """Write current state to stdout for diagnostics"""
        ...

def getSequencer() -> Sequencer: ...
@overload
def setSequencer(seq: Sequencer) -> Sequencer: ...
@overload
def setSequencer(seq: None) -> None: ...
