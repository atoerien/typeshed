from _typeshed import FileDescriptorOrPath, SupportsWrite
from collections.abc import Callable
from io import BufferedReader
from multiprocessing import Process
from multiprocessing.queues import Queue
from multiprocessing.synchronize import Event
from signal import Signals
from types import FrameType, TracebackType
from typing import IO, Any
from typing_extensions import Never, Self

__version__: str
aliases: dict[str, Any]
DEFAULT_TEXT_ENCODING: str
GRACEFUL_SHUTDOWN_SIGNAL: Signals
TERMINATION_DELAY: float
PARTIAL_DEFAULT: bool
STDOUT_FD: int
STDERR_FD: int

def enable_old_api() -> None:
    """
    Enable backwards compatibility with the old API.

    This function is called when the :mod:`capturer` module is imported. It
    modifies the :class:`CaptureOutput` class to install method proxies for
    :func:`~PseudoTerminal.get_handle()`, :func:`~PseudoTerminal.get_bytes()`,
    :func:`~PseudoTerminal.get_lines()`, :func:`~PseudoTerminal.get_text()`,
    :func:`~PseudoTerminal.save_to_handle()` and
    :func:`~PseudoTerminal.save_to_path()`.
    """
    ...
def create_proxy_method(name: str) -> Callable[..., Any]:
    """
    Create a proxy method for use by :func:`enable_old_api()`.

    :param name: The name of the :class:`PseudoTerminal` method to call when
                 the proxy method is called.
    :returns: A proxy method (a callable) to be installed on the
              :class:`CaptureOutput` class.
    """
    ...

class MultiProcessHelper:
    """
    Helper to spawn and manipulate child processes using :mod:`multiprocessing`.

    This class serves as a base class for :class:`CaptureOutput` and
    :class:`PseudoTerminal` because both classes need the same child process
    handling logic.
    """
    processes: list[Process]
    def __init__(self) -> None: ...
    def start_child(self, target: Callable[[Event], Any]) -> None: ...
    def stop_children(self) -> None: ...
    def wait_for_children(self) -> None: ...
    def enable_graceful_shutdown(self) -> None: ...
    def raise_shutdown_request(self, signum: int, frame: FrameType | None) -> Never: ...

class CaptureOutput(MultiProcessHelper):
    """Context manager to capture the standard output and error streams."""
    chunk_size: int
    encoding: str
    merged: bool
    relay: bool
    termination_delay: float
    pseudo_terminals: list[PseudoTerminal]
    streams: list[tuple[int, Stream]]
    stdout_stream: Stream
    stderr_stream: Stream
    output: PseudoTerminal
    output_queue: Queue[tuple[Any, bytes]]
    stdout: PseudoTerminal
    stderr: PseudoTerminal
    def __init__(
        self, merged: bool = True, encoding: str = ..., termination_delay: float = ..., chunk_size: int = 1024, relay: bool = True
    ) -> None:
        """
        Initialize a :class:`CaptureOutput` object.

        :param merged: Whether to capture and relay the standard output and
                       standard error streams as one stream (a boolean,
                       defaults to :data:`True`). When this is :data:`False`
                       the ``stdout`` and ``stderr`` attributes of the
                       :class:`CaptureOutput` object are
                       :class:`PseudoTerminal` objects that can be used to
                       get at the output captured from each stream separately.
        :param encoding: The name of the character encoding used to decode the
                         captured output (a string, defaults to
                         :data:`DEFAULT_TEXT_ENCODING`).
        :param termination_delay: The number of seconds to wait before
                                  terminating the output relay process (a
                                  floating point number, defaults to
                                  :data:`TERMINATION_DELAY`).
        :param chunk_size: The maximum number of bytes to read from the
                           captured streams on each call to :func:`os.read()`
                           (an integer).
        :param relay: If this is :data:`True` (the default) then captured
                      output is relayed to the terminal or parent process,
                      if it's :data:`False` the captured output is hidden
                      (swallowed).
        """
        ...
    def initialize_stream(self, file_obj: IO[str], expected_fd: int) -> Stream:
        """
        Initialize one or more :class:`Stream` objects to capture a standard stream.

        :param file_obj: A file-like object with a ``fileno()`` method.
        :param expected_fd: The expected file descriptor of the file-like object.
        :returns: The :class:`Stream` connected to the file descriptor of the
                  file-like object.

        By default this method just initializes a :class:`Stream` object
        connected to the given file-like object and its underlying file
        descriptor (a simple one-liner).

        If however the file descriptor of the file-like object doesn't have the
        expected value (``expected_fd``) two :class:`Stream` objects will be
        created instead: One of the stream objects will be connected to the
        file descriptor of the file-like object and the other stream object
        will be connected to the file descriptor that was expected
        (``expected_fd``).

        This approach is intended to make sure that "nested" output capturing
        works as expected: Output from the current Python process is captured
        from the file descriptor of the file-like object while output from
        subprocesses is captured from the file descriptor given by
        ``expected_fd`` (because the operating system defines special semantics
        for the file descriptors with the numbers one and two that we can't
        just ignore).

        For more details refer to `issue 2 on GitHub
        <https://github.com/xolox/python-capturer/issues/2>`_.
        """
        ...
    def __enter__(self) -> Self:
        """Automatically call :func:`start_capture()` when entering a :keyword:`with` block."""
        ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> bool | None:
        """Automatically call :func:`finish_capture()` when leaving a :keyword:`with` block."""
        ...
    @property
    def is_capturing(self) -> bool:
        """:data:`True` if output is being captured, :data:`False` otherwise."""
        ...
    def start_capture(self) -> None:
        """
        Start capturing the standard output and error streams.

        :raises: :exc:`~exceptions.TypeError` when output is already being
                 captured.

        This method is called automatically when using the capture object as a
        context manager. It's provided under a separate name in case someone
        wants to extend :class:`CaptureOutput` and build their own context
        manager on top of it.
        """
        ...
    def finish_capture(self) -> None:
        """
        Stop capturing the standard output and error streams.

        This method is called automatically when using the capture object as a
        context manager. It's provided under a separate name in case someone
        wants to extend :class:`CaptureOutput` and build their own context
        manager on top of it.
        """
        ...
    def allocate_pty(
        self, relay_fd: int | None = None, output_queue: Queue[tuple[Any, bytes]] | None = None, queue_token: Any | None = None
    ) -> PseudoTerminal:
        """
        Allocate a pseudo terminal.

        Internal shortcut for :func:`start_capture()` to allocate multiple
        pseudo terminals without code duplication.
        """
        ...
    def merge_loop(self, started_event: Event) -> None:
        """
        Merge and relay output in a child process.

        This internal method is used when standard output and standard error
        are being captured separately. It's responsible for emitting each
        captured line on the appropriate stream without interleaving text
        within lines.
        """
        ...
    def get_handle(self, partial: bool = ...) -> BufferedReader:
        """
        get_handle(partial=False)
        Get the captured output as a Python file object.

        :param partial: If :data:`True` (*not the default*) the partial output
                        captured so far is returned, otherwise (*so by
                        default*) the relay process is terminated and output
                        capturing is disabled before returning the captured
                        output (the default is intended to protect unsuspecting
                        users against partial reads).
        :returns: The captured output as a Python file object. The file
                  object's current position is reset to zero before this
                  function returns.

        This method is useful when you're dealing with arbitrary amounts of
        captured data that you don't want to load into memory just so you can
        save it to a file again. In fact, in that case you might want to take a
        look at :func:`save_to_path()` and/or :func:`save_to_handle()` :-).

        .. warning:: Two caveats about the use of this method:

                     1. If partial is :data:`True` (not the default) the output
                        can end in a partial line, possibly in the middle of an
                        ANSI escape sequence or a multi byte character.

                     2. If you close this file handle you just lost your last
                        chance to get at the captured output! (calling this
                        method again will not give you a new file handle)
        """
        ...
    def get_bytes(self, partial: bool = ...) -> bytes:
        """
        get_bytes(partial=False)
        Get the captured output as binary data.

        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a binary string.
        """
        ...
    def get_lines(self, interpreted: bool = True, partial: bool = ...) -> list[str]:
        """
        get_lines(interpreted=True, partial=False)
        Get the captured output split into lines.

        :param interpreted: If :data:`True` (the default) captured output is
                            processed using :func:`.clean_terminal_output()`.
        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a list of Unicode strings.

        .. warning:: If partial is :data:`True` (not the default) the output
                     can end in a partial line, possibly in the middle of a
                     multi byte character (this may cause decoding errors).
        """
        ...
    def get_text(self, interpreted: bool = ..., partial: bool = ...) -> str:
        """
        get_text(interpreted=True, partial=False)
        Get the captured output as a single string.

        :param interpreted: If :data:`True` (the default) captured output is
                            processed using :func:`clean_terminal_output()`.
        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a Unicode string.

        .. warning:: If partial is :data:`True` (not the default) the output
                     can end in a partial line, possibly in the middle of a
                     multi byte character (this may cause decoding errors).
        """
        ...
    def save_to_handle(self, handle: SupportsWrite[bytes], partial: bool = ...) -> None:
        """
        save_to_handle(handle, partial=False)
        Save the captured output to an open file handle.

        :param handle: A writable file-like object.
        :param partial: Refer to :func:`get_handle()` for details.
        """
        ...
    def save_to_path(self, filename: FileDescriptorOrPath, partial: bool = ...) -> None:
        """
        save_to_path(filename, partial=False)
        Save the captured output to a file.

        :param filename: The pathname of the file where the captured output
                         should be written to (a string).
        :param partial: Refer to :func:`get_handle()` for details.
        """
        ...

class OutputBuffer:
    """
    Helper for :func:`CaptureOutput.merge_loop()`.

    Buffers captured output and flushes to the appropriate stream after each
    line break.
    """
    fd: int
    buffer: bytes
    def __init__(self, fd: int) -> None:
        """
        Initialize an :class:`OutputBuffer` object.

        :param fd: The number of the file descriptor where output should be
                   flushed (an integer).
        """
        ...
    def add(self, output: bytes) -> None:
        """
        Add output to the buffer and flush appropriately.

        :param output: The output to add to the buffer (a string).
        """
        ...
    def flush(self) -> None:
        """Flush any remaining buffered output to the stream."""
        ...

class PseudoTerminal(MultiProcessHelper):
    """
    Helper for :class:`CaptureOutput`.

    Manages capturing of output and exposing the captured output.
    """
    encoding: str
    termination_delay: float
    chunk_size: int
    relay_fd: int | None
    output_queue: Queue[tuple[Any, bytes]] | None
    queue_token: Any | None
    streams: list[Stream]
    master_fd: int
    slave_fd: int
    output_fd: int
    output_handle: BufferedReader
    def __init__(
        self,
        encoding: str,
        termination_delay: float,
        chunk_size: int,
        relay_fd: int | None,
        output_queue: Queue[tuple[int, bytes]] | None,
        queue_token: Any | None,
    ) -> None:
        """
        Initialize a :class:`PseudoTerminal` object.

        :param encoding: The name of the character encoding used to decode the
                         captured output (a string, defaults to
                         :data:`DEFAULT_TEXT_ENCODING`).
        :param termination_delay: The number of seconds to wait before
                                  terminating the output relay process (a
                                  floating point number, defaults to
                                  :data:`TERMINATION_DELAY`).
        :param chunk_size: The maximum number of bytes to read from the
                           captured stream(s) on each call to :func:`os.read()`
                           (an integer).
        :param relay_fd: The number of the file descriptor where captured
                         output should be relayed to (an integer or
                         :data:`None` if ``output_queue`` and ``queue_token``
                         are given).
        :param output_queue: The multiprocessing queue where captured output
                             chunks should be written to (a
                             :class:`multiprocessing.Queue` object or
                             :data:`None` if ``relay_fd`` is given).
        :param queue_token: A unique identifier added to each output chunk
                            written to the queue (any value or :data:`None` if
                            ``relay_fd`` is given).
        """
        ...
    def attach(self, stream: Stream) -> None:
        """
        Attach a stream to the pseudo terminal.

        :param stream: A :class:`Stream` object.
        """
        ...
    def start_capture(self) -> None:
        """Start the child process(es) responsible for capturing and relaying output."""
        ...
    def finish_capture(self) -> None:
        """Stop the process of capturing output and destroy the pseudo terminal."""
        ...
    def close_pseudo_terminal(self) -> None:
        """Close the pseudo terminal's master/slave file descriptors."""
        ...
    def restore_streams(self) -> None:
        """Restore the stream(s) attached to the pseudo terminal."""
        ...
    def get_handle(self, partial: bool = ...) -> BufferedReader:
        """
        get_handle(partial=False)
        Get the captured output as a Python file object.

        :param partial: If :data:`True` (*not the default*) the partial output
                        captured so far is returned, otherwise (*so by
                        default*) the relay process is terminated and output
                        capturing is disabled before returning the captured
                        output (the default is intended to protect unsuspecting
                        users against partial reads).
        :returns: The captured output as a Python file object. The file
                  object's current position is reset to zero before this
                  function returns.

        This method is useful when you're dealing with arbitrary amounts of
        captured data that you don't want to load into memory just so you can
        save it to a file again. In fact, in that case you might want to take a
        look at :func:`save_to_path()` and/or :func:`save_to_handle()` :-).

        .. warning:: Two caveats about the use of this method:

                     1. If partial is :data:`True` (not the default) the output
                        can end in a partial line, possibly in the middle of an
                        ANSI escape sequence or a multi byte character.

                     2. If you close this file handle you just lost your last
                        chance to get at the captured output! (calling this
                        method again will not give you a new file handle)
        """
        ...
    def get_bytes(self, partial: bool = ...) -> bytes:
        """
        get_bytes(partial=False)
        Get the captured output as binary data.

        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a binary string.
        """
        ...
    def get_lines(self, interpreted: bool = True, partial: bool = ...) -> list[str]:
        """
        get_lines(interpreted=True, partial=False)
        Get the captured output split into lines.

        :param interpreted: If :data:`True` (the default) captured output is
                            processed using :func:`.clean_terminal_output()`.
        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a list of Unicode strings.

        .. warning:: If partial is :data:`True` (not the default) the output
                     can end in a partial line, possibly in the middle of a
                     multi byte character (this may cause decoding errors).
        """
        ...
    def get_text(self, interpreted: bool = ..., partial: bool = ...) -> str:
        """
        get_text(interpreted=True, partial=False)
        Get the captured output as a single string.

        :param interpreted: If :data:`True` (the default) captured output is
                            processed using :func:`clean_terminal_output()`.
        :param partial: Refer to :func:`get_handle()` for details.
        :returns: The captured output as a Unicode string.

        .. warning:: If partial is :data:`True` (not the default) the output
                     can end in a partial line, possibly in the middle of a
                     multi byte character (this may cause decoding errors).
        """
        ...
    def save_to_handle(self, handle: SupportsWrite[bytes], partial: bool = ...) -> None:
        """
        save_to_handle(handle, partial=False)
        Save the captured output to an open file handle.

        :param handle: A writable file-like object.
        :param partial: Refer to :func:`get_handle()` for details.
        """
        ...
    def save_to_path(self, filename: FileDescriptorOrPath, partial: bool = ...) -> None:
        """
        save_to_path(filename, partial=False)
        Save the captured output to a file.

        :param filename: The pathname of the file where the captured output
                         should be written to (a string).
        :param partial: Refer to :func:`get_handle()` for details.
        """
        ...
    def capture_loop(self, started_event: Event) -> None:
        """
        Continuously read from the master end of the pseudo terminal and relay the output.

        This function is run in the background by :func:`start_capture()`
        using the :mod:`multiprocessing` module. It's role is to read output
        emitted on the master end of the pseudo terminal and relay this output
        to the real terminal (so the operator can see what's happening in real
        time) as well as a temporary file (for additional processing by the
        caller).
        """
        ...

class Stream:
    """
    Container for standard stream redirection logic.

    Used by :class:`CaptureOutput` to temporarily redirect the standard output
    and standard error streams.

    .. attribute:: is_redirected

       :data:`True` once :func:`redirect()` has been called, :data:`False` when
       :func:`redirect()` hasn't been called yet or :func:`restore()` has since
       been called.
    """
    fd: int
    original_fd: int
    is_redirected: bool
    def __init__(self, fd: int) -> None:
        """
        Initialize a :class:`Stream` object.

        :param fd: The file descriptor to be redirected (an integer).
        """
        ...
    def redirect(self, target_fd: int) -> None:
        """
        Redirect output written to the file descriptor to another file descriptor.

        :param target_fd: The file descriptor that should receive the output
                          written to the file descriptor given to the
                          :class:`Stream` constructor (an integer).
        :raises: :exc:`~exceptions.TypeError` when the file descriptor is
                 already being redirected.
        """
        ...
    def restore(self) -> None:
        """Stop redirecting output written to the file descriptor."""
        ...

class ShutdownRequested(Exception):
    """
    Raised by :func:`~MultiProcessHelper.raise_shutdown_request()` to signal
    graceful termination requests (in :func:`~PseudoTerminal.capture_loop()`).
    """
    ...
