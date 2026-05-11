import sys
import time
from collections.abc import Callable, Sequence
from typing import IO, Any, TypeAlias

__all__ = ["Timer", "timeit", "repeat", "default_timer"]

_Timer: TypeAlias = Callable[[], float]
_Stmt: TypeAlias = str | Callable[[], object]

default_timer: _Timer

class Timer:
    """
    Class for timing execution speed of small code snippets.

    The constructor takes a statement to be timed, an additional
    statement used for setup, and a timer function.  Both statements
    default to 'pass'; the timer function is platform-dependent (see
    module doc string).  If 'globals' is specified, the code will be
    executed within that namespace (as opposed to inside timeit's
    namespace).

    To measure the execution time of the first statement, use the
    timeit() method.  The repeat() method is a convenience to call
    timeit() multiple times and return a list of results.

    The statements may contain newlines, as long as they don't contain
    multi-line string literals.
    """
    def __init__(
        self,
        stmt: _Stmt = "pass",
        setup: _Stmt = "pass",
        timer: _Timer = time.perf_counter,
        globals: dict[str, Any] | None = None,
    ) -> None: ...
    def print_exc(self, file: IO[str] | None = None) -> None: ...
    def timeit(self, number: int = 1000000) -> float: ...
    def repeat(self, repeat: int = 5, number: int = 1000000) -> list[float]: ...
    if sys.version_info >= (3, 15):
        def autorange(
            self, callback: Callable[[int, float], object] | None = None, target_time: float = 0.2
        ) -> tuple[int, float]: ...
    else:
        def autorange(self, callback: Callable[[int, float], object] | None = None) -> tuple[int, float]: ...

def timeit(
    stmt: _Stmt = "pass",
    setup: _Stmt = "pass",
    timer: _Timer = time.perf_counter,
    number: int = 1000000,
    globals: dict[str, Any] | None = None,
) -> float:
    """Convenience function to create Timer object and call timeit method."""
    ...
def repeat(
    stmt: _Stmt = "pass",
    setup: _Stmt = "pass",
    timer: _Timer = time.perf_counter,
    repeat: int = 5,
    number: int = 1000000,
    globals: dict[str, Any] | None = None,
) -> list[float]:
    """Convenience function to create Timer object and call repeat method."""
    ...
def main(args: Sequence[str] | None = None, *, _wrap_timer: Callable[[_Timer], _Timer] | None = None) -> None:
    """
    Main program, used when run as a script.

    The optional 'args' argument specifies the command line to be parsed,
    defaulting to sys.argv[1:].

    The return value is an exit code to be passed to sys.exit(); it
    may be None to indicate success.

    When an exception happens during timing, a traceback is printed to
    stderr and the return value is 1.  Exceptions at other times
    (including the template compilation) are not caught.

    '_wrap_timer' is an internal interface used for unit testing.  If it
    is not None, it must be a callable that accepts a timer function
    and returns another timer function (used for unit testing).
    """
    ...
