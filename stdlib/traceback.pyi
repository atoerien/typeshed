"""Extract, format and print information about Python stack traces."""

import sys
from _typeshed import SupportsWrite, Unused
from collections.abc import Generator, Iterable, Iterator, Mapping
from types import FrameType, TracebackType
from typing import Any, ClassVar, Literal, SupportsIndex, TypeAlias, overload
from typing_extensions import Self, deprecated

__all__ = [
    "extract_stack",
    "extract_tb",
    "format_exception",
    "format_exception_only",
    "format_list",
    "format_stack",
    "format_tb",
    "print_exc",
    "format_exc",
    "print_exception",
    "print_last",
    "print_stack",
    "print_tb",
    "clear_frames",
    "FrameSummary",
    "StackSummary",
    "TracebackException",
    "walk_stack",
    "walk_tb",
]

if sys.version_info >= (3, 14):
    __all__ += ["print_list"]

_FrameSummaryTuple: TypeAlias = tuple[str, int, str, str | None]

def print_tb(tb: TracebackType | None, limit: int | None = None, file: SupportsWrite[str] | None = None) -> None: ...
@overload
def print_exception(
    exc: type[BaseException] | None,
    /,
    value: BaseException | None = ...,
    tb: TracebackType | None = ...,
    limit: int | None = None,
    file: SupportsWrite[str] | None = None,
    chain: bool = True,
) -> None: ...
@overload
def print_exception(
    exc: BaseException, /, *, limit: int | None = None, file: SupportsWrite[str] | None = None, chain: bool = True
) -> None: ...
@overload
def format_exception(
    exc: type[BaseException] | None,
    /,
    value: BaseException | None = ...,
    tb: TracebackType | None = ...,
    limit: int | None = None,
    chain: bool = True,
) -> list[str]: ...
@overload
def format_exception(exc: BaseException, /, *, limit: int | None = None, chain: bool = True) -> list[str]: ...
def print_exc(limit: int | None = None, file: SupportsWrite[str] | None = None, chain: bool = True) -> None: ...
def print_last(limit: int | None = None, file: SupportsWrite[str] | None = None, chain: bool = True) -> None: ...
def print_stack(f: FrameType | None = None, limit: int | None = None, file: SupportsWrite[str] | None = None) -> None: ...
def extract_tb(tb: TracebackType | None, limit: int | None = None) -> StackSummary: ...
def extract_stack(f: FrameType | None = None, limit: int | None = None) -> StackSummary: ...
def format_list(extracted_list: Iterable[FrameSummary | _FrameSummaryTuple]) -> list[str]: ...
def print_list(extracted_list: Iterable[FrameSummary | _FrameSummaryTuple], file: SupportsWrite[str] | None = None) -> None: ...

if sys.version_info >= (3, 13):
    @overload
    def format_exception_only(exc: BaseException | None, /, *, show_group: bool = False) -> list[str]:
        """
        Format the exception part of a traceback.

        The return value is a list of strings, each ending in a newline.

        The list contains the exception's message, which is
        normally a single string; however, for :exc:`SyntaxError` exceptions, it
        contains several lines that (when printed) display detailed information
        about where the syntax error occurred. Following the message, the list
        contains the exception's ``__notes__``.

        When *show_group* is ``True``, and the exception is an instance of
        :exc:`BaseExceptionGroup`, the nested exceptions are included as
        well, recursively, with indentation relative to their nesting depth.
        """
        ...
    @overload
    def format_exception_only(exc: Unused, /, value: BaseException | None, *, show_group: bool = False) -> list[str]:
        """
        Format the exception part of a traceback.

        The return value is a list of strings, each ending in a newline.

        The list contains the exception's message, which is
        normally a single string; however, for :exc:`SyntaxError` exceptions, it
        contains several lines that (when printed) display detailed information
        about where the syntax error occurred. Following the message, the list
        contains the exception's ``__notes__``.

        When *show_group* is ``True``, and the exception is an instance of
        :exc:`BaseExceptionGroup`, the nested exceptions are included as
        well, recursively, with indentation relative to their nesting depth.
        """
        ...

else:
    @overload
    def format_exception_only(exc: BaseException | None, /) -> list[str]:
        """
        Format the exception part of a traceback.

        The return value is a list of strings, each ending in a newline.

        The list contains the exception's message, which is
        normally a single string; however, for :exc:`SyntaxError` exceptions, it
        contains several lines that (when printed) display detailed information
        about where the syntax error occurred. Following the message, the list
        contains the exception's ``__notes__``.
        """
        ...
    @overload
    def format_exception_only(exc: Unused, /, value: BaseException | None) -> list[str]:
        """
        Format the exception part of a traceback.

        The return value is a list of strings, each ending in a newline.

        The list contains the exception's message, which is
        normally a single string; however, for :exc:`SyntaxError` exceptions, it
        contains several lines that (when printed) display detailed information
        about where the syntax error occurred. Following the message, the list
        contains the exception's ``__notes__``.
        """
        ...

def format_exc(limit: int | None = None, chain: bool = True) -> str: ...
def format_tb(tb: TracebackType | None, limit: int | None = None) -> list[str]: ...
def format_stack(f: FrameType | None = None, limit: int | None = None) -> list[str]: ...
def clear_frames(tb: TracebackType | None) -> None: ...
def walk_stack(f: FrameType | None) -> Iterator[tuple[FrameType, int]]: ...
def walk_tb(tb: TracebackType | None) -> Iterator[tuple[FrameType, int]]: ...

if sys.version_info >= (3, 11):
    class _ExceptionPrintContext:
        def indent(self) -> str: ...
        def emit(self, text_gen: str | Iterable[str], margin_char: str | None = None) -> Generator[str]: ...

class TracebackException:
    """
    An exception ready for rendering.

    The traceback module captures enough attributes from the original exception
    to this intermediary form to ensure that no references are held, while
    still being able to fully print or format it.

    max_group_width and max_group_depth control the formatting of exception
    groups. The depth refers to the nesting level of the group, and the width
    refers to the size of a single exception group's exceptions array. The
    formatted output is truncated when either limit is exceeded.

    Use `from_exception` to create TracebackException instances from exception
    objects, or the constructor to create TracebackException instances from
    individual components.

    - :attr:`__cause__` A TracebackException of the original *__cause__*.
    - :attr:`__context__` A TracebackException of the original *__context__*.
    - :attr:`exceptions` For exception groups - a list of TracebackException
      instances for the nested *exceptions*.  ``None`` for other exceptions.
    - :attr:`__suppress_context__` The *__suppress_context__* value from the
      original exception.
    - :attr:`stack` A `StackSummary` representing the traceback.
    - :attr:`exc_type` (deprecated) The class of the original traceback.
    - :attr:`exc_type_str` String display of exc_type
    - :attr:`filename` For syntax errors - the filename where the error
      occurred.
    - :attr:`lineno` For syntax errors - the linenumber where the error
      occurred.
    - :attr:`end_lineno` For syntax errors - the end linenumber where the error
      occurred. Can be `None` if not present.
    - :attr:`text` For syntax errors - the text where the error
      occurred.
    - :attr:`offset` For syntax errors - the offset into the text where the
      error occurred.
    - :attr:`end_offset` For syntax errors - the end offset into the text where
      the error occurred. Can be `None` if not present.
    - :attr:`msg` For syntax errors - the compiler error message.
    """
    __cause__: TracebackException | None
    __context__: TracebackException | None
    if sys.version_info >= (3, 11):
        exceptions: list[TracebackException] | None
    __suppress_context__: bool
    if sys.version_info >= (3, 11):
        __notes__: list[str] | None
    stack: StackSummary

    # These fields only exist for `SyntaxError`s, but there is no way to express that in the type system.
    filename: str
    lineno: str | None
    end_lineno: str | None
    text: str
    offset: int
    end_offset: int | None
    msg: str

    if sys.version_info >= (3, 13):
        @property
        def exc_type_str(self) -> str: ...
        @property
        @deprecated("Deprecated since Python 3.13. Use `exc_type_str` instead.")
        def exc_type(self) -> type[BaseException] | None: ...
    else:
        exc_type: type[BaseException]
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType | None,
            *,
            limit: int | None = None,
            lookup_lines: bool = True,
            capture_locals: bool = False,
            compact: bool = False,
            max_group_width: int = 15,
            max_group_depth: int = 10,
            save_exc_type: bool = True,
            _seen: set[int] | None = None,
        ) -> None: ...
    elif sys.version_info >= (3, 11):
        def __init__(
            self,
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType | None,
            *,
            limit: int | None = None,
            lookup_lines: bool = True,
            capture_locals: bool = False,
            compact: bool = False,
            max_group_width: int = 15,
            max_group_depth: int = 10,
            _seen: set[int] | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType | None,
            *,
            limit: int | None = None,
            lookup_lines: bool = True,
            capture_locals: bool = False,
            compact: bool = False,
            _seen: set[int] | None = None,
        ) -> None: ...

    if sys.version_info >= (3, 11):
        @classmethod
        def from_exception(
            cls,
            exc: BaseException,
            *,
            limit: int | None = None,
            lookup_lines: bool = True,
            capture_locals: bool = False,
            compact: bool = False,
            max_group_width: int = 15,
            max_group_depth: int = 10,
        ) -> Self: ...
    else:
        @classmethod
        def from_exception(
            cls,
            exc: BaseException,
            *,
            limit: int | None = None,
            lookup_lines: bool = True,
            capture_locals: bool = False,
            compact: bool = False,
        ) -> Self: ...

    def __eq__(self, other: object) -> bool: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]
    if sys.version_info >= (3, 11):
        def format(self, *, chain: bool = True, _ctx: _ExceptionPrintContext | None = None) -> Generator[str]:
            """
            Format the exception.

            If chain is not *True*, *__cause__* and *__context__* will not be formatted.

            The return value is a generator of strings, each ending in a newline and
            some containing internal newlines. `print_exception` is a wrapper around
            this method which just prints the lines to a file.

            The message indicating which exception occurred is always the last
            string in the output.
            """
            ...
    else:
        def format(self, *, chain: bool = True) -> Generator[str]:
            """
            Format the exception.

            If chain is not *True*, *__cause__* and *__context__* will not be formatted.

            The return value is a generator of strings, each ending in a newline and
            some containing internal newlines. `print_exception` is a wrapper around
            this method which just prints the lines to a file.

            The message indicating which exception occurred is always the last
            string in the output.
            """
            ...

    if sys.version_info >= (3, 13):
        def format_exception_only(self, *, show_group: bool = False, _depth: int = 0) -> Generator[str]:
            """
            Format the exception part of the traceback.

            The return value is a generator of strings, each ending in a newline.

            Generator yields the exception message.
            For :exc:`SyntaxError` exceptions, it
            also yields (before the exception message)
            several lines that (when printed)
            display detailed information about where the syntax error occurred.
            Following the message, generator also yields
            all the exception's ``__notes__``.

            When *show_group* is ``True``, and the exception is an instance of
            :exc:`BaseExceptionGroup`, the nested exceptions are included as
            well, recursively, with indentation relative to their nesting depth.
            """
            ...
    else:
        def format_exception_only(self) -> Generator[str]:
            """
            Format the exception part of the traceback.

            The return value is a generator of strings, each ending in a newline.

            Generator yields the exception message.
            For :exc:`SyntaxError` exceptions, it
            also yields (before the exception message)
            several lines that (when printed)
            display detailed information about where the syntax error occurred.
            Following the message, generator also yields
            all the exception's ``__notes__``.
            """
            ...

    if sys.version_info >= (3, 11):
        def print(self, *, file: SupportsWrite[str] | None = None, chain: bool = True) -> None:
            """Print the result of self.format(chain=chain) to 'file'."""
            ...

class FrameSummary:
    """
    Information about a single frame from a traceback.

    - :attr:`filename` The filename for the frame.
    - :attr:`lineno` The line within filename for the frame that was
      active when the frame was captured.
    - :attr:`name` The name of the function or method that was executing
      when the frame was captured.
    - :attr:`line` The text from the linecache module for the
      of code that was running when the frame was captured.
    - :attr:`locals` Either None if locals were not supplied, or a dict
      mapping the name to the repr() of the variable.
    """
    if sys.version_info >= (3, 13):
        __slots__ = (
            "filename",
            "lineno",
            "end_lineno",
            "colno",
            "end_colno",
            "name",
            "_lines",
            "_lines_dedented",
            "locals",
            "_code",
        )
    elif sys.version_info >= (3, 11):
        __slots__ = ("filename", "lineno", "end_lineno", "colno", "end_colno", "name", "_line", "locals")
    else:
        __slots__ = ("filename", "lineno", "name", "_line", "locals")
    if sys.version_info >= (3, 11):
        def __init__(
            self,
            filename: str,
            lineno: int | None,
            name: str,
            *,
            lookup_line: bool = True,
            locals: Mapping[str, str] | None = None,
            line: str | None = None,
            end_lineno: int | None = None,
            colno: int | None = None,
            end_colno: int | None = None,
        ) -> None:
            """
            Construct a FrameSummary.

            :param lookup_line: If True, `linecache` is consulted for the source
                code line. Otherwise, the line will be looked up when first needed.
            :param locals: If supplied the frame locals, which will be captured as
                object representations.
            :param line: If provided, use this instead of looking up the line in
                the linecache.
            """
            ...
        end_lineno: int | None
        colno: int | None
        end_colno: int | None
    else:
        def __init__(
            self,
            filename: str,
            lineno: int | None,
            name: str,
            *,
            lookup_line: bool = True,
            locals: Mapping[str, str] | None = None,
            line: str | None = None,
        ) -> None:
            """
            Construct a FrameSummary.

            :param lookup_line: If True, `linecache` is consulted for the source
                code line. Otherwise, the line will be looked up when first needed.
            :param locals: If supplied the frame locals, which will be captured as
                object representations.
            :param line: If provided, use this instead of looking up the line in
                the linecache.
            """
            ...
    filename: str
    lineno: int | None
    name: str
    locals: dict[str, str] | None
    @property
    def line(self) -> str | None: ...
    @overload
    def __getitem__(self, pos: Literal[0]) -> str: ...
    @overload
    def __getitem__(self, pos: Literal[1]) -> int: ...
    @overload
    def __getitem__(self, pos: Literal[2]) -> str: ...
    @overload
    def __getitem__(self, pos: Literal[3]) -> str | None: ...
    @overload
    def __getitem__(self, pos: SupportsIndex) -> Any: ...
    @overload
    def __getitem__(self, pos: slice[SupportsIndex | None]) -> tuple[Any, ...]: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __eq__(self, other: object) -> bool: ...
    def __len__(self) -> Literal[4]: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]

class StackSummary(list[FrameSummary]):
    """A list of FrameSummary objects, representing a stack of frames."""
    @classmethod
    def extract(
        cls,
        frame_gen: Iterable[tuple[FrameType, int]],
        *,
        limit: int | None = None,
        lookup_lines: bool = True,
        capture_locals: bool = False,
    ) -> StackSummary:
        """
        Create a StackSummary from a traceback or stack object.

        :param frame_gen: A generator that yields (frame, lineno) tuples
            whose summaries are to be included in the stack.
        :param limit: None to include all frames or the number of frames to
            include.
        :param lookup_lines: If True, lookup lines for each frame immediately,
            otherwise lookup is deferred until the frame is rendered.
        :param capture_locals: If True, the local variables from each frame will
            be captured as object representations into the FrameSummary.
        """
        ...
    @classmethod
    def from_list(cls, a_list: Iterable[FrameSummary | _FrameSummaryTuple]) -> StackSummary:
        """
        Create a StackSummary object from a supplied list of
        FrameSummary objects or old-style list of tuples.
        """
        ...
    if sys.version_info >= (3, 11):
        def format_frame_summary(self, frame_summary: FrameSummary) -> str:
            """
            Format the lines for a single FrameSummary.

            Returns a string representing one frame involved in the stack. This
            gets called for every frame to be printed in the stack summary.
            """
            ...

    def format(self) -> list[str]:
        """
        Format the stack ready for printing.

        Returns a list of strings ready for printing.  Each string in the
        resulting list corresponds to a single frame from the stack.
        Each string ends in a newline; the strings may contain internal
        newlines as well, for those items with source text lines.

        For long sequences of the same frame and line, the first few
        repetitions are shown, followed by a summary line stating the exact
        number of further repetitions.
        """
        ...
