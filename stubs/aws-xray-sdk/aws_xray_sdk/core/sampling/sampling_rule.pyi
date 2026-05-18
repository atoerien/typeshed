from typing import Literal, TypedDict, type_check_only

from .reservoir import Reservoir

@type_check_only
class _Stats(TypedDict):
    request_count: int
    borrow_count: int
    sampled_count: int

class SamplingRule:
    """Data model for a single centralized sampling rule definition."""
    def __init__(
        self, name: str, priority, rate, reservoir_size, host=None, method=None, path=None, service=None, service_type=None
    ) -> None: ...
    def match(self, sampling_req) -> bool:
        """
        Determines whether or not this sampling rule applies to the incoming
        request based on some of the request's parameters.
        Any ``None`` parameter provided will be considered an implicit match.
        """
        ...
    def is_default(self) -> bool: ...
    def snapshot_statistics(self) -> _Stats:
        """
        Take a snapshot of request/borrow/sampled count for reporting
        back to X-Ray back-end by ``TargetPoller`` and reset those counters.
        """
        ...
    def merge(self, rule) -> None:
        """Migrate all stateful attributes from the old rule"""
        ...
    def ever_matched(self) -> bool:
        """
        Returns ``True`` if this sample rule has ever been matched
        with an incoming request within the reporting interval.
        """
        ...
    def time_to_report(self) -> Literal[True] | None:
        """
        Returns ``True`` if it is time to report sampling statistics
        of this rule to refresh quota information for its reservoir.
        """
        ...
    def increment_request_count(self) -> None: ...
    def increment_borrow_count(self) -> None: ...
    def increment_sampled_count(self) -> None: ...

    @property
    def rate(self): ...
    @rate.setter
    def rate(self, v) -> None: ...

    @property
    def name(self) -> str: ...
    @property
    def priority(self): ...

    @property
    def reservoir(self) -> Reservoir: ...
    @reservoir.setter
    def reservoir(self, v: Reservoir) -> None: ...

    @property
    def can_borrow(self) -> bool: ...
    @property
    def request_count(self) -> int: ...
    @property
    def borrow_count(self) -> int: ...
    @property
    def sampled_count(self) -> int: ...
