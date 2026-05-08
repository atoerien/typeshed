from collections.abc import Callable
from queue import Queue
from threading import Lock, Thread
from typing import ClassVar, Literal, TypeAlias

from ._keyboard_event import KeyboardEvent
from ._mouse_event import _MouseEvent

_Event: TypeAlias = KeyboardEvent | _MouseEvent

class GenericListener:
    lock: ClassVar[Lock]
    handlers: list[Callable[[_Event], bool | None]]
    listening: bool
    queue: Queue[_Event]
    listening_thread: Thread | None
    processing_thread: Thread | None
    def invoke_handlers(self, event: _Event) -> Literal[1] | None: ...
    def start_if_necessary(self) -> None:
        """Starts the listening thread if it wasn't already."""
        ...
    def pre_process_event(self, event: _Event) -> None: ...
    def process(self) -> None:
        """Loops over the underlying queue of events and processes them in order."""
        ...
    def add_handler(self, handler: Callable[[_Event], bool | None]) -> None:
        """
        Adds a function to receive each event captured, starting the capturing
        process if necessary.
        """
        ...
    def remove_handler(self, handler: Callable[[_Event], bool | None]) -> None:
        """Removes a previously added event handler. """
        ...
