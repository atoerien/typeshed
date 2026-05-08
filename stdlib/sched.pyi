import time
from collections.abc import Callable
from typing import Any, NamedTuple, TypeAlias

__all__ = ["scheduler"]

_ActionCallback: TypeAlias = Callable[..., Any]

class Event(NamedTuple):
    time: float
    priority: Any
    sequence: int
    action: _ActionCallback
    argument: tuple[Any, ...]
    kwargs: dict[str, Any]

class scheduler:
    timefunc: Callable[[], float]
    delayfunc: Callable[[float], object]

    def __init__(
        self, timefunc: Callable[[], float] = time.monotonic, delayfunc: Callable[[float], object] = time.sleep
    ) -> None:
        """
        Initialize a new instance, passing the time and delay
        functions
        """
        ...
    def enterabs(
        self, time: float, priority: Any, action: _ActionCallback, argument: tuple[Any, ...] = (), kwargs: dict[str, Any] = ...
    ) -> Event:
        """
        Enter a new event in the queue at an absolute time.

        Returns an ID for the event which can be used to remove it,
        if necessary.
        """
        ...
    def enter(
        self, delay: float, priority: Any, action: _ActionCallback, argument: tuple[Any, ...] = (), kwargs: dict[str, Any] = ...
    ) -> Event:
        """
        A variant that specifies the time as a relative time.

        This is actually the more commonly used interface.
        """
        ...
    def run(self, blocking: bool = True) -> float | None:
        """
        Execute events until the queue is empty.
        If blocking is False executes the scheduled events due to
        expire soonest (if any) and then return the deadline of the
        next scheduled call in the scheduler.

        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.

        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.

        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.
        """
        ...
    def cancel(self, event: Event) -> None:
        """
        Remove an event from the queue.

        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.
        """
        ...
    def empty(self) -> bool:
        """Check whether the queue is empty."""
        ...
    @property
    def queue(self) -> list[Event]:
        """
        An ordered list of upcoming events.

        Events are named tuples with fields for:
            time, priority, action, arguments, kwargs
        """
        ...
