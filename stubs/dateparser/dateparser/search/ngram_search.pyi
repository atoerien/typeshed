"""
Date search based on parsing token n-grams.

This module implements an alternative strategy for
:func:`dateparser.search.search_dates` that looks for the longest sequences
of tokens that can be parsed as dates. It originates from a production date
extraction pipeline where it consistently produced more predictable results
than the translation-based search.
"""

import datetime
from _typeshed import Incomplete
from collections.abc import Set as AbstractSet
from logging import Logger

from dateparser.conf import Settings

logger: Logger

class _NgramDateSearch:
    """
    Search for dates by trying to parse token n-grams, longest first.

    The text is split into tokens using characters that never occur inside
    a date expression as separators. The tokens are then scanned left to
    right; at each position the longest n-gram (up to ``max_tokens``
    tokens) is tried first, so that the most complete date is parsed.
    Whenever an n-gram is parsed successfully, the scan continues after it,
    so the reported dates never overlap.
    """
    max_tokens: int
    def __init__(self, max_tokens: int = 7) -> None: ...
    def search_parse(
        self,
        languages: list[str] | tuple[str, ...] | AbstractSet[str] | None,
        text: str,
        settings: Settings | dict[str, Incomplete] | None,
    ) -> list[tuple[str, datetime.datetime]]:
        """
        Find all dates in ``text`` and return ``(substring, date)`` pairs.

        ``languages`` are tried in the given order for every candidate
        n-gram.
        """
        ...
