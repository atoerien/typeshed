"""
JACK Client for Python.

http://jackclient-python.readthedocs.io/
"""

from _typeshed import Unused
from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from typing import Any, Final, Literal, NoReturn, overload, type_check_only
from typing_extensions import Self

import numpy
from _cffi_backend import _CDataBase
from numpy.typing import NDArray

# Aka jack_position_t
# Actual type: _cffi_backend.__CDataOwn <cdata 'struct _jack_position *'>
# This is not a real subclassing. Just ensuring type-checkers sees this type as compatible with _CDataBase
# pyright has no error code for subclassing final
@type_check_only
class _JackPositionT(_CDataBase):  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
    audio_frames_per_video_frame: float
    bar: int
    bar_start_tick: float
    bbt_offset: int
    beat: int
    beat_type: float
    beats_per_bar: float
    beats_per_minute: float
    frame: int
    frame_rate: int
    frame_time: float
    next_time: float
    padding: _CDataBase  # <cdata 'int32_t[7]'>
    tick: int
    ticks_per_beat: float
    unique_1: int
    unique_2: int
    usecs: int
    valid: int
    video_offset: int

@type_check_only
class _CBufferType:
    @overload
    def __getitem__(self, key: int) -> str: ...
    @overload
    def __getitem__(self, key: slice) -> bytes: ...
    @overload
    def __setitem__(self, key: int, val: str) -> None: ...
    @overload
    def __setitem__(self, key: slice, val: bytes) -> None: ...
    def __len__(self) -> int: ...
    def __bytes__(self) -> bytes: ...

STOPPED: int
ROLLING: int
STARTING: int
NETSTARTING: int
PROPERTY_CREATED: int
PROPERTY_CHANGED: int
PROPERTY_DELETED: int
POSITION_BBT: int
POSITION_TIMECODE: int
POSITION_BBT_FRAME_OFFSET: int
POSITION_AUDIO_VIDEO_RATIO: int
POSITION_VIDEO_FRAME_OFFSET: int

class JackError(Exception):
    """Exception for all kinds of JACK-related errors."""
    ...

class JackErrorCode(JackError):
    def __init__(self, message: str, code: int) -> None:
        """
        Exception for JACK errors with an error code.

        Subclass of `JackError`.

        The following attributes are available:

        Attributes
        ----------
        message
            Error message.
        code
            The error code returned by the JACK library function which
            resulted in this exception being raised.
        """
        ...
    message: str
    code: int

class JackOpenError(JackError):
    def __init__(self, name: str, status: Status) -> None:
        """
        Exception raised for errors while creating a JACK client.

        Subclass of `JackError`.

        The following attributes are available:

        Attributes
        ----------
        name
            Requested client name.
        status
            A :class:`Status` instance representing the status information
            received by the ``jack_client_open()`` JACK library call.
        """
        ...
    name: str
    status: Status

class Client:
    """A client that can connect to the JACK audio server."""
    def __init__(
        self,
        name: str,
        use_exact_name: bool = False,
        no_start_server: bool = False,
        servername: str | None = None,
        session_id: str | None = None,
    ) -> None:
        """
        Create a new JACK client.

        A client object is a *context manager*, i.e. it can be used in a
        *with statement* to automatically call `activate()` in the
        beginning of the statement and `deactivate()` and `close()` on
        exit.

        Parameters
        ----------
        name : str
            The desired client name of at most `client_name_size()`
            characters.  The name scope is local to each server.
            Unless forbidden by the *use_exact_name* option, the server
            will modify this name to create a unique variant, if needed.

        Other Parameters
        ----------------
        use_exact_name : bool
            Whether an error should be raised if *name* is not unique.
            See `Status.name_not_unique`.
        no_start_server : bool
            Do not automatically start the JACK server when it is not
            already running.  This option is always selected if
            ``JACK_NO_START_SERVER`` is defined in the calling process
            environment.
        servername : str
            Selects from among several possible concurrent server
            instances.
            Server names are unique to each user.  If unspecified, use
            ``'default'`` unless ``JACK_DEFAULT_SERVER`` is defined in
            the process environment.
        session_id : str
            Pass a SessionID Token. This allows the sessionmanager to
            identify the client again.

        Raises
        ------
        JackOpenError
            If the session with the JACK server could not be opened.
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused) -> None: ...
    def __del__(self) -> None:
        """Close JACK client on garbage collection."""
        ...
    @property
    def name(self) -> str:
        """The name of the JACK client (read-only)."""
        ...
    @property
    def uuid(self) -> str:
        """
        The UUID of the JACK client (read-only).

        Raises
        ------
        JackError
            If getting the UUID fails.
        """
        ...
    @property
    def samplerate(self) -> int:
        """The sample rate of the JACK system (read-only)."""
        ...
    @property
    def blocksize(self) -> int:
        """
        The JACK block size (must be a power of two).

        The current maximum size that will ever be passed to the process
        callback.  It should only be queried *before* `activate()` has
        been called.  This size may change, clients that depend on it
        must register a callback with `set_blocksize_callback()` so they
        will be notified if it does.

        Changing the blocksize stops the JACK engine process cycle, then
        calls all registered callback functions (see
        `set_blocksize_callback()`) before restarting the process
        cycle.  This will cause a gap in the audio flow, so it should
        only be done at appropriate stopping points.
        """
        ...
    @blocksize.setter
    def blocksize(self, blocksize: int) -> None:
        """
        The JACK block size (must be a power of two).

        The current maximum size that will ever be passed to the process
        callback.  It should only be queried *before* `activate()` has
        been called.  This size may change, clients that depend on it
        must register a callback with `set_blocksize_callback()` so they
        will be notified if it does.

        Changing the blocksize stops the JACK engine process cycle, then
        calls all registered callback functions (see
        `set_blocksize_callback()`) before restarting the process
        cycle.  This will cause a gap in the audio flow, so it should
        only be done at appropriate stopping points.
        """
        ...
    @property
    def status(self) -> Status:
        """JACK client status.  See `Status`."""
        ...
    @property
    def realtime(self) -> bool:
        """Whether JACK is running with ``-R`` (``--realtime``)."""
        ...
    @property
    def frames_since_cycle_start(self) -> int:
        """
        Time since start of audio block.

        The estimated time in frames that has passed since the JACK
        server began the current process cycle.
        """
        ...
    @property
    def frame_time(self) -> int:
        """
        The estimated current time in frames.

        This is intended for use in other threads (not the process
        callback).  The return value can be compared with the value of
        `last_frame_time` to relate time in other threads to JACK time.
        """
        ...
    @property
    def last_frame_time(self) -> int:
        """
        The precise time at the start of the current process cycle.

        This may only be used from the process callback (see
        `set_process_callback()`), and can be used to interpret
        timestamps generated by `frame_time` in other threads with
        respect to the current process cycle.

        This is the only jack time function that returns exact time:
        when used during the process callback it always returns the same
        value (until the next process callback, where it will return
        that value + `blocksize`, etc).  The return value is guaranteed
        to be monotonic and linear in this fashion unless an xrun occurs
        (see `set_xrun_callback()`).  If an xrun occurs, clients must
        check this value again, as time may have advanced in a
        non-linear way (e.g.  cycles may have been skipped).
        """
        ...
    @property
    def inports(self) -> Ports:
        """
        A list of audio input `Ports`.

        New ports can be created and added to this list with
        `inports.register() <Ports.register>`.
        When :meth:`~OwnPort.unregister` is called on one of the items
        in this list, this port is removed from the list.
        `inports.clear() <Ports.clear>` can be used to unregister all
        audio input ports at once.

        See Also
        --------
        Ports, OwnPort
        """
        ...
    @property
    def outports(self) -> Ports:
        """
        A list of audio output :class:`Ports`.

        New ports can be created and added to this list with
        `outports.register() <Ports.register>`.
        When :meth:`~OwnPort.unregister` is called on one of the items
        in this list, this port is removed from the list.
        `outports.clear() <Ports.clear>` can be used to unregister all
        audio output ports at once.

        See Also
        --------
        Ports, OwnPort
        """
        ...
    @property
    def midi_inports(self) -> Ports:
        """
        A list of MIDI input :class:`Ports`.

        New MIDI ports can be created and added to this list with
        `midi_inports.register() <Ports.register>`.
        When :meth:`~OwnPort.unregister` is called on one of the items
        in this list, this port is removed from the list.
        `midi_inports.clear() <Ports.clear>` can be used to unregister
        all MIDI input ports at once.

        See Also
        --------
        Ports, OwnMidiPort
        """
        ...
    @property
    def midi_outports(self) -> Ports:
        """
        A list of MIDI output :class:`Ports`.

        New MIDI ports can be created and added to this list with
        `midi_outports.register() <Ports.register>`.
        When :meth:`~OwnPort.unregister` is called on one of the items
        in this list, this port is removed from the list.
        `midi_outports.clear() <Ports.clear>` can be used to unregister
        all MIDI output ports at once.

        See Also
        --------
        Ports, OwnMidiPort
        """
        ...
    def owns(self, port: str | Port) -> bool:
        """
        Check if a given port belongs to *self*.

        Parameters
        ----------
        port : str or Port
            Full port name or `Port`, `MidiPort`, `OwnPort` or
            `OwnMidiPort` object.
        """
        ...
    def activate(self) -> None:
        """
        Activate JACK client.

        Tell the JACK server that the program is ready to start
        processing audio.
        """
        ...
    def deactivate(self, ignore_errors: bool = True) -> None:
        """
        De-activate JACK client.

        Tell the JACK server to remove *self* from the process graph.
        Also, disconnect all ports belonging to it, since inactive
        clients have no port connections.
        """
        ...
    def cpu_load(self) -> float:
        """
        Return the current CPU load estimated by JACK.

        This is a running average of the time it takes to execute a full
        process cycle for all clients as a percentage of the real time
        available per cycle determined by `blocksize` and `samplerate`.
        """
        ...
    def close(self, ignore_errors: bool = True) -> None:
        """Close the JACK client."""
        ...
    def connect(self, source: str | Port, destination: str | Port) -> None:
        """
        Establish a connection between two ports.

        When a connection exists, data written to the source port will
        be available to be read at the destination port.

        Audio ports can obviously not be connected with MIDI ports.

        Parameters
        ----------
        source : str or Port
            One end of the connection. Must be an output port.
        destination : str or Port
            The other end of the connection. Must be an input port.

        See Also
        --------
        OwnPort.connect, disconnect

        Raises
        ------
        JackError
            If there is already an existing connection between *source* and
            *destination* or the connection can not be established.
        """
        ...
    def disconnect(self, source: str | Port, destination: str | Port) -> None:
        """
        Remove a connection between two ports.

        Parameters
        ----------
        source, destination : str or Port
            See `connect()`.
        """
        ...
    def transport_start(self) -> None:
        """Start JACK transport."""
        ...
    def transport_stop(self) -> None:
        """Stop JACK transport."""
        ...
    @property
    def transport_state(self) -> TransportState:
        """
        JACK transport state.

        This is one of `STOPPED`, `ROLLING`, `STARTING`, `NETSTARTING`.

        See Also
        --------
        transport_query
        """
        ...
    @property
    def transport_frame(self) -> int:
        """
        Get/set current JACK transport frame.

        Return an estimate of the current transport frame, including any
        time elapsed since the last transport positional update.
        Assigning a frame number repositions the JACK transport.
        """
        ...
    @transport_frame.setter
    def transport_frame(self, frame: int) -> None:
        """
        Get/set current JACK transport frame.

        Return an estimate of the current transport frame, including any
        time elapsed since the last transport positional update.
        Assigning a frame number repositions the JACK transport.
        """
        ...
    def transport_locate(self, frame: int) -> None:
        """
        .. deprecated:: 0.4.1
            Use `transport_frame` instead
        """
        ...
    def transport_query(self) -> tuple[TransportState, dict[str, Any]]:
        """
        Query the current transport state and position.

        This is a convenience function that does the same as
        `transport_query_struct()`, but it only returns the valid fields
        in an easy-to-use ``dict``.

        Returns
        -------
        state : TransportState
            The transport state can take following values:
            `STOPPED`, `ROLLING`, `STARTING` and `NETSTARTING`.
        position : dict
            A dictionary containing only the valid fields of the
            structure returned by `transport_query_struct()`.

        See Also
        --------
        :attr:`transport_state`, transport_query_struct
        """
        ...
    def transport_query_struct(self) -> tuple[TransportState, _JackPositionT]:
        """
        Query the current transport state and position.

        This function is realtime-safe, and can be called from any
        thread.  If called from the process thread, the returned
        position corresponds to the first frame of the current cycle and
        the state returned is valid for the entire cycle.

        Returns
        -------
        state : int
            The transport state can take following values: `STOPPED`,
            `ROLLING`, `STARTING` and `NETSTARTING`.
        position : jack_position_t
            See the `JACK transport documentation`__ for the available
            fields.

            __ https://jackaudio.org/api/structjack__position__t.html

        See Also
        --------
        transport_query, transport_reposition_struct
        """
        ...
    def transport_reposition_struct(self, position: _JackPositionT) -> None:
        """
        Request a new transport position.

        May be called at any time by any client.  The new position takes
        effect in two process cycles.  If there are slow-sync clients
        and the transport is already rolling, it will enter the
        `STARTING` state and begin invoking their sync callbacks
        (see `set_sync_callback()`) until ready.
        This function is realtime-safe.

        Parameters
        ----------
        position : jack_position_t
            Requested new transport position.  This is the same
            structure as returned by `transport_query_struct()`.

        See Also
        --------
        transport_query_struct, transport_locate
        """
        ...
    def set_sync_timeout(self, timeout: int) -> None:
        """
        Set the timeout value for slow-sync clients.

        This timeout prevents unresponsive slow-sync clients from
        completely halting the transport mechanism.  The default is two
        seconds.  When the timeout expires, the transport starts
        rolling, even if some slow-sync clients are still unready.
        The *sync callbacks* of these clients continue being invoked,
        giving them a chance to catch up.

        Parameters
        ----------
        timeout : int
            Delay (in microseconds) before the timeout expires.

        See Also
        --------
        set_sync_callback
        """
        ...
    def set_freewheel(self, onoff: bool) -> None:
        """
        Start/Stop JACK's "freewheel" mode.

        When in "freewheel" mode, JACK no longer waits for any external
        event to begin the start of the next process cycle.

        As a result, freewheel mode causes "faster than realtime"
        execution of a JACK graph. If possessed, real-time scheduling is
        dropped when entering freewheel mode, and if appropriate it is
        reacquired when stopping.

        IMPORTANT: on systems using capabilities to provide real-time
        scheduling (i.e. Linux kernel 2.4), if onoff is zero, this
        function must be called from the thread that originally called
        `activate()`.  This restriction does not apply to other systems
        (e.g. Linux kernel 2.6 or OS X).

        Parameters
        ----------
        onoff : bool
            If ``True``, freewheel mode starts. Otherwise freewheel mode
            ends.

        See Also
        --------
        set_freewheel_callback
        """
        ...
    def set_shutdown_callback(self, callback: Callable[[Status, str], object]) -> None:
        """
        Register shutdown callback.

        Register a function (and optional argument) to be called if and
        when the JACK server shuts down the client thread.
        The function must be written as if it were an asynchonrous POSIX
        signal handler -- use only async-safe functions, and remember
        that it is executed from another thread.
        A typical function might set a flag or write to a pipe so that
        the rest of the application knows that the JACK client thread
        has shut down.

        .. note:: Clients do not need to call this.  It exists only to
           help more complex clients understand what is going on.  It
           should be called before `activate()`.

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever the JACK
            daemon is shutdown.  It must have this signature::

                callback(status: Status, reason: str) -> None

            The argument *status* is of type `jack.Status`.

            .. note:: The *callback* should typically signal another
               thread to correctly finish cleanup by calling `close()`
               (since it cannot be called directly in the context of the
               thread that calls the shutdown callback).

               After server shutdown, the client is *not* deallocated by
               JACK, the user (that's you!) is responsible to properly
               use `close()` to release client ressources.
               Alternatively, the `Client` object can be used as a
               *context manager* in a *with statement*, which takes care
               of activating, deactivating and closing the client
               automatically.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        """
        ...
    def set_process_callback(self, callback: Callable[[int], object]) -> None:
        """
        Register process callback.

        Tell the JACK server to call *callback* whenever there is work
        be done.

        The code in the supplied function must be suitable for real-time
        execution.  That means that it cannot call functions that might
        block for a long time. This includes malloc, free, printf,
        pthread_mutex_lock, sleep, wait, poll, select, pthread_join,
        pthread_cond_wait, etc, etc.

        .. warning:: Most Python interpreters use a `global interpreter
           lock (GIL)`__, which violates the above real-time
           requirement.  Furthermore, Python's `garbage collector`__
           might become active at an inconvenient time and block the
           process callback for some time.

           Because of this, Python is not really suitable for real-time
           processing.  If you want to implement a *reliable* real-time
           audio/MIDI application, you should use a different
           programming language, such as C or C++.

           If you can live with some random audio drop-outs now and
           then, feel free to continue using Python!

        __ https://en.wikipedia.org/wiki/Global_Interpreter_Lock
        __ https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called by the engine anytime
            there is work to be done.  It must have this signature::

                callback(frames: int) -> None

            The argument *frames* specifies the number of frames that
            have to be processed in the current audio block.
            It will be the same number as `blocksize` and it will be a
            power of two.

            As long as the client is active, the *callback* will be
            called once in each process cycle.  However, if an exception
            is raised inside of a *callback*, it will not be called
            anymore.  The exception `CallbackExit` can be used to
            silently prevent further callback invocations, all other
            exceptions will print an error message to *stderr*.
        """
        ...
    def set_freewheel_callback(self, callback: Callable[[bool], object]) -> None:
        """
        Register freewheel callback.

        Tell the JACK server to call *callback* whenever we enter or
        leave "freewheel" mode.
        The argument to the callback will be ``True`` if JACK is
        entering freewheel mode, and ``False`` otherwise.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever JACK starts
            or stops freewheeling.  It must have this signature::

                callback(starting: bool) -> None

            The argument *starting* is ``True`` if we start to
            freewheel, ``False`` otherwise.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.

        See Also
        --------
        set_freewheel
        """
        ...
    def set_blocksize_callback(self, callback: Callable[[int], object]) -> None:
        """
        Register blocksize callback.

        Tell JACK to call *callback* whenever the size of the the buffer
        that will be passed to the process callback is about to change.
        Clients that depend on knowing the buffer size must supply a
        *callback* before activating themselves.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is invoked whenever the JACK
            engine buffer size changes.  It must have this signature::

                callback(blocksize: int) -> None

            The argument *blocksize* is the new buffer size.
            The *callback* is supposed to raise `CallbackExit` on error.

            .. note:: Although this function is called in the JACK
               process thread, the normal process cycle is suspended
               during its operation, causing a gap in the audio flow.
               So, the *callback* can allocate storage, touch memory not
               previously referenced, and perform other operations that
               are not realtime safe.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.

        See Also
        --------
        :attr:`blocksize`
        """
        ...
    def set_samplerate_callback(self, callback: Callable[[int], object]) -> None:
        """
        Register samplerate callback.

        Tell the JACK server to call *callback* whenever the system
        sample rate changes.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called when the engine sample
            rate changes.  It must have this signature::

                callback(samplerate: int) -> None

            The argument *samplerate* is the new engine sample rate.
            The *callback* is supposed to raise `CallbackExit` on error.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.

        See Also
        --------
        :attr:`samplerate`
        """
        ...
    def set_client_registration_callback(self, callback: Callable[[str, bool], object]) -> None:
        """
        Register client registration callback.

        Tell the JACK server to call *callback* whenever a client is
        registered or unregistered.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever a client is
            registered or unregistered.  It must have this signature::

                callback(name: str, register: bool) -> None

            The first argument contains the client name, the second
            argument is ``True`` if the client is being registered and
            ``False`` if the client is being unregistered.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        """
        ...
    def set_port_registration_callback(
        self, callback: Callable[[Port, bool], object] | None = None, only_available: bool = True
    ) -> None:
        """
        Register port registration callback.

        Tell the JACK server to call *callback* whenever a port is
        registered or unregistered.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        .. note:: Due to JACK 1 behavior, it is not possible to get
           the pointer to an unregistering JACK Port if it already
           existed before `activate()` was called. This will cause
           the callback not to be called if *only_available* is
           ``True``, or called with ``None`` as first argument (see
           below).

           To avoid this, call `Client.get_ports()` just after
           `activate()`, allowing the module to store pointers to
           already existing ports and always receive a `Port`
           argument for this callback.

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever a port is
            registered or unregistered.  It must have this signature::

                callback(port: Port, register: bool) -> None

            The first argument is a `Port`, `MidiPort`, `OwnPort` or
            `OwnMidiPort` object, the second argument is ``True`` if the
            port is being registered, ``False`` if the port is being
            unregistered.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        only_available : bool, optional
            If ``True``, the *callback* is not called if the port in
            question is not available anymore (after another JACK client
            has unregistered it).
            If ``False``, it is called nonetheless, but the first
            argument of the *callback* will be ``None`` if the port is
            not available anymore.

        See Also
        --------
        Ports.register
        """
        ...
    def set_port_connect_callback(
        self, callback: Callable[[Port, Port, bool], object] | None = None, only_available: bool = True
    ) -> None:
        """
        Register port connect callback.

        Tell the JACK server to call *callback* whenever a port is
        connected or disconnected.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        .. note:: Due to JACK 1 behavior, it is not possible to get
           the pointer to an unregistering JACK Port if it already
           existed before `activate()` was called. This will cause
           the callback not to be called if *only_available* is
           ``True``, or called with ``None`` as first argument (see
           below).

           To avoid this, call `Client.get_ports()` just after
           `activate()`, allowing the module to store pointers to
           already existing ports and always receive a `Port`
           argument for this callback.

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever a port is
            connected or disconnected.  It must have this signature::

                callback(a: Port, b: Port, connect: bool) -> None

            The first and second arguments contain `Port`, `MidiPort`,
            `OwnPort` or `OwnMidiPort` objects of the ports which are
            connected or disconnected.  The third argument is ``True``
            if the ports were connected and ``False`` if the ports were
            disconnected.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        only_available : bool, optional
            See `set_port_registration_callback()`.
            If ``False``, the first and/or the second argument to the
            *callback* may be ``None``.

        See Also
        --------
        Client.connect, OwnPort.connect
        """
        ...
    def set_port_rename_callback(
        self, callback: Callable[[Port, str, str], object] | None = None, only_available: bool = True
    ) -> None:
        """
        Register port rename callback.

        Tell the JACK server to call *callback* whenever a port is
        renamed.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever the port name
            has been changed.  It must have this signature::

                callback(port: Port, old: str, new: str) -> None

            The first argument is the port that has been renamed (a
            `Port`, `MidiPort`, `OwnPort` or `OwnMidiPort` object); the
            second and third argument is the old and new name,
            respectively.  The *callback* is supposed to raise
            `CallbackExit` on error.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        only_available : bool, optional
            See `set_port_registration_callback()`.

        See Also
        --------
        :attr:`Port.shortname`

        Notes
        -----
        The port rename callback is not available in JACK 1!
        See and `this commit message`__.

        __ https://github.com/jackaudio/jack1/commit/
           94c819accfab2612050e875c24cf325daa0fd26d
        """
        ...
    def set_graph_order_callback(self, callback: Callable[[], object]) -> None:
        """
        Register graph order callback.

        Tell the JACK server to call *callback* whenever the processing
        graph is reordered.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after :meth:`activate` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever the
            processing graph is reordered.
            It must have this signature::

                callback() -> None

            The *callback* is supposed to raise `CallbackExit` on error.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        """
        ...
    def set_xrun_callback(self, callback: Callable[[float], object]) -> None:
        """
        Register xrun callback.

        Tell the JACK server to call *callback* whenever there is an
        xrun.

        All "notification events" are received in a separated non RT
        thread, the code in the supplied function does not need to be
        suitable for real-time execution.

        .. note:: This function cannot be called while the client is
           activated (after `activate()` has been called).

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever an xrun has
            occured.  It must have this signature::

                callback(delayed_usecs: float) -> None

            The callback argument is the delay in microseconds due to
            the most recent XRUN occurrence.
            The *callback* is supposed to raise `CallbackExit` on error.

            .. note:: Same as with most callbacks, no functions that
               interact with the JACK daemon should be used here.
        """
        ...
    def set_sync_callback(self, callback: Callable[[int, _JackPositionT], object] | None) -> None:
        """
        Register (or unregister) as a slow-sync client.

        A slow-sync client is one that cannot respond immediately to
        transport position changes.

        The *callback* will be invoked at the first available
        opportunity after its registration is complete.  If the client
        is currently active this will be the following process cycle,
        otherwise it will be the first cycle after calling `activate()`.
        After that, it runs whenever some client requests a new
        position, or the transport enters the `STARTING` state.
        While the client is active, this callback is invoked just before
        the *process callback* (see `set_process_callback()`) in the
        same thread.

        Clients that don't set a *sync callback* are assumed to be ready
        immediately any time the transport wants to start.

        Parameters
        ----------
        callback : callable or None

            User-supplied function that returns ``True`` when the
            slow-sync client is ready.  This realtime function must not
            wait.  It must have this signature::

                callback(state: int, pos: jack_position_t) -> bool

            The *state* argument will be:

            - `STOPPED` when a new position is requested;
            - `STARTING` when the transport is waiting to start;
            - `ROLLING` when the timeout has expired, and the position
              is now a moving target.

            The *pos* argument holds the new transport position using
            the same structure as returned by
            `transport_query_struct()`.

            Setting *callback* to ``None`` declares that this
            client no longer requires slow-sync processing.

        See Also
        --------
        set_sync_timeout
        """
        ...
    def release_timebase(self) -> None:
        """
        De-register as timebase master.

        Should be called by the current timebase master to release
        itself from that responsibility and to stop the callback
        registered with `set_timebase_callback()` from being called.

        If the timebase master releases the timebase or leaves the JACK
        graph for any reason, the JACK engine takes over at the start of
        the next process cycle. The transport state does not change. If
        rolling, it continues to play, with frame numbers as the only
        available position information.

        Raises
        ------
        JackError
            If the client is not the current timebase master or
            releasing the timebase failed for another reason

        See Also
        --------
        set_timebase_callback
        """
        ...
    def set_timebase_callback(
        self, callback: Callable[[int, int, _JackPositionT, bool], object] | None = None, conditional: bool = False
    ) -> bool:
        """
        Register as timebase master for the JACK subsystem.

        The timebase master registers a callback that updates extended
        position information such as beats or timecode whenever
        necessary.  Without this extended information, there is no need
        for this function.

        There is never more than one master at a time.  When a new
        client takes over, the former callback is no longer called.
        Taking over the timebase may be done conditionally, so that
        *callback* is not registered if there was a master already.

        Parameters
        ----------
        callback : callable
            Realtime function that returns extended position
            information.  Its output affects all of the following
            process cycle.  This realtime function must not wait.
            It is called immediately after the process callback (see
            `set_process_callback()`) in the same thread whenever the
            transport is rolling, or when any client has requested a new
            position in the previous cycle.  The first cycle after
            `set_timebase_callback()` is also treated as a new position,
            or the first cycle after `activate()` if the client had been
            inactive.  The *callback* must have this signature::

                callback(
                    state: int,
                    blocksize: int,
                    pos: jack_position_t,
                    new_pos: bool,
                ) -> None

            state
                The current transport state.  See `transport_state`.
            blocksize
                The number of frames in the current period.
                See `blocksize`.
            pos
                The position structure for the next cycle; ``pos.frame``
                will be its frame number.  If *new_pos* is ``False``,
                this structure contains extended position information
                from the current cycle.  If *new_pos* is ``True``, it
                contains whatever was set by the requester.
                The *callback*'s task is to update the extended
                information here.  See `transport_query_struct()`
                for details about ``jack_position_t``.
            new_pos
                ``True`` for a newly requested *pos*, or for the first
                cycle after the timebase callback is defined.

            .. note:: The *pos* argument must not be used to set
               ``pos.frame``.  To change position, use
               `transport_reposition_struct()` or `transport_locate()`.
               These functions are realtime-safe, the timebase callback
               can call them directly.
        conditional : bool
            Set to ``True`` for a conditional request.

        Returns
        -------
        bool
            ``True`` if the timebase callback was registered.
            ``False`` if a conditional request failed because another
            timebase master is already registered.
        """
        ...
    def set_property_change_callback(self, callback: Callable[[int, str, int], object]) -> None:
        """
        Register property change callback.

        Tell the JACK server to call *callback* whenever a property is
        created, changed or deleted.

        Parameters
        ----------
        callback : callable
            User-supplied function that is called whenever a property is
            created, changed or deleted.  It must have this signature::

                callback(subject: int, key: str, change: int) -> None

            The first and second arguments are the *subject* and *key*,
            respectively.  See `set_property()` for details.
            The third argument has one of the values `PROPERTY_CREATED`,
            `PROPERTY_CHANGED` or `PROPERTY_DELETED`, which should be
            self-explanatory.
        """
        ...
    def get_uuid_for_client_name(self, name: str) -> str:
        """
        Get the session ID for a client name.

        The session manager needs this to reassociate a client name to
        the session ID.

        Raises
        ------
        JackError
            If no client with the given name exists.
        """
        ...
    def get_client_name_by_uuid(self, uuid: str) -> str:
        """
        Get the client name for a session ID.

        In order to snapshot the graph connections, the session manager
        needs to map session IDs to client names.

        Raises
        ------
        JackError
            If no client with the given UUID exists.
        """
        ...
    def get_port_by_name(self, name: str) -> Port:
        """
        Get port by name.

        Given a full port name, this returns a `Port`, `MidiPort`,
        `OwnPort` or `OwnMidiPort` object.

        Raises
        ------
        JackError
            If no port with the given name exists.
        """
        ...
    def get_all_connections(self, port: Port) -> list[Port]:
        """
        Return a list of ports which the given port is connected to.

        This differs from `OwnPort.connections` (also available on
        `OwnMidiPort`) in two important respects:

        1) You may not call this function from code that is executed in
           response to a JACK event. For example, you cannot use it in a
           graph order callback.

        2) You need not be the owner of the port to get information
           about its connections.
        """
        ...
    def get_ports(
        self,
        name_pattern: str = "",
        is_audio: bool = False,
        is_midi: bool = False,
        is_input: bool = False,
        is_output: bool = False,
        is_physical: bool = False,
        can_monitor: bool = False,
        is_terminal: bool = False,
    ) -> list[Port]:
        """
        Return a list of selected ports.

        Parameters
        ----------
        name_pattern : str
            A regular expression used to select ports by name.  If
            empty, no selection based on name will be carried out.
        is_audio, is_midi : bool
            Select audio/MIDI ports.  If neither of them is ``True``,
            both types of ports are selected.
        is_input, is_output, is_physical, can_monitor, is_terminal : bool
            Select ports by their flags.  If none of them are ``True``,
            no selection based on flags will be carried out.

        Returns
        -------
        list of Port/MidiPort/OwnPort/OwnMidiPort
            All ports that satisfy the given conditions.
        """
        ...
    def set_property(self, subject: int | str, key: str, value: str | bytes, type: str = "") -> None:
        """
        Set a metadata property on *subject*.

        Parameters
        ----------
        subject : int or str
            The subject (UUID) to set the property on.
            UUIDs can be obtained with `Client.uuid`, `Port.uuid` and
            `Client.get_uuid_for_client_name()`.
        key : str
            The key (URI) of the property.  Some predefined keys are
            available as ``jack.METADATA_*`` module constants.
        value : str or bytes
            The value of the property.
        type : str, optional
            The type of the property, either a MIME type or URI.
            If *type* is empty, the *value* is assumed to be a UTF-8
            encoded string (``'text/plain'``).

            Example values:

            - ``'image/png;base64'`` (base64 encoded PNG image)
            - ``'http://www.w3.org/2001/XMLSchema#int'`` (integer)

            Official types are preferred, but clients may use any
            syntactically valid MIME type (which start with a type and
            slash, like ``'text/...'``).  If a URI type is used, it must
            be a complete absolute URI (which start with a scheme and
            colon, like ``'http:'``).

        See Also
        --------
        get_property
        get_properties
        get_all_properties
        remove_property
        remove_properties
        remove_all_properties
        set_property_change_callback
        """
        ...
    def remove_property(self, subject: int | str, key: str) -> None:
        """
        Remove a single metadata property on *subject*.

        Parameters
        ----------
        subject : int or str
            The subject (UUID) to remove the property from.
            UUIDs can be obtained with `Client.uuid`, `Port.uuid` and
            `Client.get_uuid_for_client_name()`.
        key : str
            The key of the property to be removed.

        See Also
        --------
        set_property
        get_property
        get_properties
        get_all_properties
        remove_properties
        remove_all_properties
        set_property_change_callback
        """
        ...
    def remove_properties(self, subject: int | str) -> int:
        """
        Remove all metadata properties on *subject*.

        Parameters
        ----------
        subject : int or str
            The subject (UUID) to remove all properties from.
            UUIDs can be obtained with `Client.uuid`, `Port.uuid` and
            `Client.get_uuid_for_client_name()`.

        Returns
        -------
        int
            The number of properties removed.

        See Also
        --------
        set_property
        get_property
        get_properties
        get_all_properties
        remove_property
        remove_all_properties
        set_property_change_callback
        """
        ...
    def remove_all_properties(self) -> None:
        """
        Remove all metadata properties.

        .. warning::

            This deletes all metadata managed by a running JACK server.
            Data lost cannot be recovered (though it can be recreated by
            new calls to `set_property()`).

        See Also
        --------
        set_property
        get_property
        get_properties
        get_all_properties
        remove_property
        remove_properties
        set_property_change_callback
        """
        ...

class Port:
    """
    A JACK audio port.

    This class cannot be instantiated directly.  Instead, instances of
    this class are returned from `Client.get_port_by_name()`,
    `Client.get_ports()`, `Client.get_all_connections()` and
    `OwnPort.connections`.
    In addition, instances of this class are available in the callbacks
    which are set with `Client.set_port_registration_callback()`,
    `Client.set_port_connect_callback()` or
    `Client.set_port_rename_callback`.

    Note, however, that if the used `Client` owns the respective port,
    instances of `OwnPort` (instead of `Port`) will be created.  In case
    of MIDI ports, instances of `MidiPort` or `OwnMidiPort` are created.

    Besides being the type of non-owned JACK audio ports, this class
    also serves as base class for all other port classes (`OwnPort`,
    `MidiPort` and `OwnMidiPort`).

    New JACK audio/MIDI ports can be created with the
    :meth:`~Ports.register` method of `Client.inports`,
    `Client.outports`, `Client.midi_inports` and `Client.midi_outports`.
    """
    # <cdata 'struct _jack_port *'>
    def __init__(self, port_ptr: _CDataBase, client: Client) -> None: ...
    def __eq__(self, other: object) -> bool:
        """Ports are equal if their underlying port pointers are."""
        ...
    def __ne__(self, other: object) -> bool:
        """This should be implemented whenever __eq__() is implemented."""
        ...
    @property
    def name(self) -> str:
        """Full name of the JACK port (read-only)."""
        ...
    @property
    def shortname(self) -> str:
        """
        Short name of the JACK port, not including the client name.

        Must be unique among all ports owned by a client.

        May be modified at any time.  If the resulting full name
        (including the ``client_name:`` prefix) is longer than
        `port_name_size()`, it will be truncated.
        """
        ...
    @shortname.setter
    def shortname(self, shortname: str) -> None:
        """
        Short name of the JACK port, not including the client name.

        Must be unique among all ports owned by a client.

        May be modified at any time.  If the resulting full name
        (including the ``client_name:`` prefix) is longer than
        `port_name_size()`, it will be truncated.
        """
        ...
    @property
    def aliases(self) -> list[str]:
        """Returns a list of strings with the aliases for the JACK port."""
        ...
    def set_alias(self, alias: str) -> None:
        """
        Set an alias for the JACK port.

        Ports can have up to two aliases. If both are already set,
        this function will return an error.
        """
        ...
    def unset_alias(self, alias: str) -> None:
        """
        Remove an alias for the JACK port.

        If the alias doesn't exist this function will return an error.
        """
        ...
    @property
    def uuid(self) -> int:
        """The UUID of the JACK port."""
        ...
    @property
    def is_audio(self) -> bool:
        """This is always ``True``."""
        ...
    @property
    def is_midi(self) -> bool:
        """This is always ``False``."""
        ...
    @property
    def is_input(self) -> bool:
        """Can the port receive data?"""
        ...
    @property
    def is_output(self) -> bool:
        """Can data be read from this port?"""
        ...
    @property
    def is_physical(self) -> bool:
        """Does it correspond to some kind of physical I/O connector?"""
        ...
    @property
    def can_monitor(self) -> bool:
        """Does a call to `request_monitor()` make sense?"""
        ...
    @property
    def is_terminal(self) -> bool:
        """Is the data consumed/generated?"""
        ...
    def request_monitor(self, onoff: bool) -> None:
        """
        Set input monitoring.

        If `can_monitor` is ``True``, turn input monitoring on or
        off.  Otherwise, do nothing.

        Parameters
        ----------
        onoff : bool
            If ``True``, switch monitoring on; if ``False``, switch it
            off.
        """
        ...

class MidiPort(Port):
    """
    A JACK MIDI port.

    This class is derived from `Port` and has exactly the same
    attributes and methods.

    This class cannot be instantiated directly (see `Port`).

    New JACK audio/MIDI ports can be created with the
    :meth:`~Ports.register` method of `Client.inports`,
    `Client.outports`, `Client.midi_inports` and `Client.midi_outports`.

    See Also
    --------
    Port, OwnMidiPort
    """
    @property
    def is_audio(self) -> Literal[False]:
        """This is always ``False``."""
        ...
    @property
    def is_midi(self) -> Literal[True]:
        """This is always ``True``."""
        ...

class OwnPort(Port):
    """
    A JACK audio port owned by a `Client`.

    This class is derived from `Port`.  `OwnPort` objects can do
    everything that `Port` objects can, plus a lot more.

    This class cannot be instantiated directly (see `Port`).

    New JACK audio/MIDI ports can be created with the
    :meth:`~Ports.register` method of `Client.inports`,
    `Client.outports`, `Client.midi_inports` and `Client.midi_outports`.
    """
    @property
    def number_of_connections(self) -> int:
        """Number of connections to or from port."""
        ...
    @property
    def connections(self) -> list[Port]:
        """List of ports which the port is connected to."""
        ...
    def is_connected_to(self, port: str | Port) -> bool:
        """
        Am I *directly* connected to *port*?

        Parameters
        ----------
        port : str or Port
            Full port name or port object.
        """
        ...
    def connect(self, port: str | Port) -> None:
        """
        Connect to given port.

        Parameters
        ----------
        port : str or Port
            Full port name or port object.

        See Also
        --------
        Client.connect
        """
        ...
    def disconnect(self, other: str | Port | None = None) -> None:
        """
        Disconnect this port.

        Parameters
        ----------
        other : str or Port
            Port to disconnect from.
            By default, disconnect from all connected ports.
        """
        ...
    def unregister(self) -> None:
        """
        Unregister port.

        Remove the port from the client, disconnecting any existing
        connections.  This also removes the port from
        `Client.inports`, `Client.outports`, `Client.midi_inports` or
        `Client.midi_outports`.
        """
        ...
    def get_buffer(self) -> _CBufferType:
        """
        Get buffer for audio data.

        This returns a buffer holding the memory area associated with
        the specified port.  For an output port, it will be a memory
        area that can be written to; for an input port, it will be an
        area containing the data from the port's connection(s), or
        zero-filled.  If there are multiple inbound connections, the
        data will be mixed appropriately.

        Caching output ports is DEPRECATED in JACK 2.0, due to some new
        optimization (like "pipelining").  Port buffers have to be
        retrieved in each callback for proper functioning.

        This method shall only be called from within the process
        callback (see `Client.set_process_callback()`).
        """
        ...
    def get_array(self) -> NDArray[numpy.float32]:
        """
        Get audio buffer as NumPy array.

        Make sure to ``import numpy`` before calling this, otherwise the
        first call might take a long time.

        This method shall only be called from within the process
        callback (see `Client.set_process_callback()`).

        See Also
        --------
        get_buffer
        """
        ...

class OwnMidiPort(MidiPort, OwnPort):
    """
    A JACK MIDI port owned by a `Client`.

    This class is derived from `OwnPort` and `MidiPort`, which are
    themselves derived from `Port`.  It has the same attributes and
    methods as `OwnPort`, but `get_buffer()` and `get_array()` are
    disabled.  Instead, it has methods for sending and receiving MIDI
    events (to be used only from within the process callback -- see
    `Client.set_process_callback()`).

    This class cannot be instantiated directly (see `Port`).

    New JACK audio/MIDI ports can be created with the
    :meth:`~Ports.register` method of `Client.inports`,
    `Client.outports`, `Client.midi_inports` and `Client.midi_outports`.
    """
    def __init__(self, port_ptr: _CDataBase, client: Client) -> None: ...
    # The implementation raises NotImplementedError, but this is not an abstract class.
    # `get_buffer()` and `get_array()` are disabled for OwnMidiPort
    def get_buffer(self) -> NoReturn:
        """Not available for MIDI ports."""
        ...
    def get_array(self) -> NoReturn:
        """Not available for MIDI ports."""
        ...
    @property
    def max_event_size(self) -> int:
        """
        Get the size of the largest event that can be stored by the port.

        This returns the current space available, taking into
        account events already stored in the port.
        """
        ...
    @property
    def lost_midi_events(self) -> int:
        """
        Get the number of events that could not be written to the port.

        This being a non-zero value implies that the port is full.
        Currently the only way this can happen is if events are lost on
        port mixdown.
        """
        ...
    def incoming_midi_events(self) -> Generator[tuple[int, _CBufferType], None, None]:
        """
        Return generator for incoming MIDI events.

        JACK MIDI is normalised, the MIDI events yielded by this
        generator are guaranteed to be complete MIDI events (the status
        byte will always be present, and no realtime events will be
        interspersed with the events).

        Yields
        ------
        time : int
            Time (in samples) relative to the beginning of the current
            audio block.
        event : buffer
            The actual MIDI event data.

            .. warning:: The buffer is re-used (and therefore
               overwritten) between iterations.  If you want to keep the
               data beyond the current iteration, please make a copy.
        """
        ...
    def clear_buffer(self) -> None:
        """
        Clear an event buffer.

        This should be called at the beginning of each process cycle
        before calling `reserve_midi_event()` or `write_midi_event()`.
        This function may not be called on an input port.
        """
        ...
    def write_midi_event(self, time: int, event: bytes | Sequence[int] | _CBufferType) -> None:
        """
        Create an outgoing MIDI event.

        Clients must write normalised MIDI data to the port - no running
        status and no (one-byte) realtime messages interspersed with
        other messages (realtime messages are fine when they occur on
        their own, like other messages).

        Events must be written in order, sorted by their sample offsets.
        JACK will not sort the events for you, and will refuse to store
        out-of-order events.

        Parameters
        ----------
        time : int
            Time (in samples) relative to the beginning of the current
            audio block.
        event : bytes or buffer or sequence of int
            The actual MIDI event data.

            .. note:: Buffer objects are only supported for CFFI >= 0.9.

        Raises
        ------
        JackError
            If MIDI event couldn't be written.
        """
        ...
    def reserve_midi_event(self, time: int, size: int) -> _CBufferType:
        """
        Get a buffer where an outgoing MIDI event can be written to.

        Clients must write normalised MIDI data to the port - no running
        status and no (one-byte) realtime messages interspersed with
        other messages (realtime messages are fine when they occur on
        their own, like other messages).

        Events must be written in order, sorted by their sample offsets.
        JACK will not sort the events for you, and will refuse to store
        out-of-order events.

        Parameters
        ----------
        time : int
            Time (in samples) relative to the beginning of the current
            audio block.
        size : int
            Number of bytes to reserve.

        Returns
        -------
        buffer
            A buffer object where MIDI data bytes can be written to.
            If no space could be reserved, an empty buffer is returned.
        """
        ...

class Ports:
    """
    A list of input/output ports.

    This class is not meant to be instantiated directly.  It is only
    used as `Client.inports`, `Client.outports`, `Client.midi_inports`
    and `Client.midi_outports`.

    The ports can be accessed by indexing or by iteration.

    New ports can be added with `register()`, existing ports can be
    removed by calling their :meth:`~OwnPort.unregister` method.
    """
    def __init__(self, client: Client, porttype: str, flag: int) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, name: str) -> Port: ...
    def __iter__(self) -> Iterator[Port]: ...
    def register(self, shortname: str, is_terminal: bool = False, is_physical: bool = False) -> Port:
        """
        Create a new input/output port.

        The new `OwnPort` or `OwnMidiPort` object is automatically added
        to `Client.inports`, `Client.outports`, `Client.midi_inports` or
        `Client.midi_outports`.

        Parameters
        ----------
        shortname : str
            Each port has a short name.  The port's full name contains
            the name of the client concatenated with a colon (:)
            followed by its short name.  The `port_name_size()` is the
            maximum length of this full name.  Exceeding that will cause
            the port registration to fail.

            The port name must be unique among all ports owned by this
            client.
            If the name is not unique, the registration will fail.
        is_terminal : bool
            For an input port: If ``True``, the data received by the
            port will not be passed on or made available at any other
            port.
            For an output port: If ``True``, the data available at the
            port does not originate from any other port

            Audio synthesizers, I/O hardware interface clients, HDR
            systems are examples of clients that would set this flag for
            their ports.
        is_physical : bool
            If ``True`` the port corresponds to some kind of physical
            I/O connector.

        Returns
        -------
        Port
            A new `OwnPort` or `OwnMidiPort` instance.
        """
        ...
    def clear(self) -> None:
        """
        Unregister all ports in the list.

        See Also
        --------
        OwnPort.unregister
        """
        ...

class RingBuffer:
    """JACK's lock-free ringbuffer."""
    def __init__(self, size: int) -> None:
        """
        Create a lock-free ringbuffer.

        A ringbuffer is a good way to pass data between threads
        (e.g. between the main program and the process callback),
        when streaming realtime data to slower media, like audio file
        playback or recording.

        The key attribute of a ringbuffer is that it can be safely
        accessed by two threads simultaneously -- one reading from the
        buffer and the other writing to it -- without using any
        synchronization or mutual exclusion primitives.  For this to
        work correctly, there can only be a single reader and a single
        writer thread.  Their identities cannot be interchanged.

        Parameters
        ----------
        size : int
            Size in bytes.  JACK will allocate a buffer of at least this
            size (rounded up to the next power of 2), but one byte is
            reserved for internal use.  Use `write_space` to
            determine the actual size available for writing.


        Raises
        ------
        JackError
            If the rightbufefr could not be allocated.
        """
        ...
    @property
    def write_space(self) -> int:
        """The number of bytes available for writing."""
        ...
    def write(self, data: bytes | Iterable[int] | _CBufferType) -> int:
        """
        Write data into the ringbuffer.

        Parameters
        ----------
        data : buffer or bytes or iterable of int
            Bytes to be written to the ringbuffer.

        Returns
        -------
        int
            The number of bytes written, which could be less than the
            length of *data* if there was no more space left
            (see `write_space`).

        See Also
        --------
        :attr:`write_space`, :attr:`write_buffers`
        """
        ...
    @property
    def write_buffers(self) -> tuple[_CBufferType, _CBufferType]:
        """
        Contains two buffer objects that can be written to directly.

        Two are needed because the space available for writing may be
        split across the end of the ringbuffer.  Either of them could be
        0 length.

        This can be used as a no-copy version of `write()`.

        When finished with writing, `write_advance()` should be used.

        .. note:: After an operation that changes the write pointer
           (`write()`, `write_advance()`, `reset()`), the buffers are no
           longer valid and one should use this property again to get
           new ones.
        """
        ...
    def write_advance(self, size: int) -> None:
        """
        Advance the write pointer.

        After data has been written to the ringbuffer using
        `write_buffers`, use this method to advance the buffer pointer,
        making the data available for future read operations.

        Parameters
        ----------
        size : int
            The number of bytes to advance.
        """
        ...
    @property
    def read_space(self) -> int:
        """The number of bytes available for reading."""
        ...
    def read(self, size: int) -> _CBufferType:
        """
        Read data from the ringbuffer.

        Parameters
        ----------
        size : int
            Number of bytes to read.

        Returns
        -------
        buffer
            A buffer object containing the requested data.
            If no more data is left (see `read_space`), a smaller
            (or even empty) buffer is returned.

        See Also
        --------
        peek, :attr:`read_space`, :attr:`read_buffers`
        """
        ...
    def peek(self, size: int) -> _CBufferType:
        """
        Peek at data from the ringbuffer.

        Opposed to `read()` this function does not move the read
        pointer.  Thus it's a convenient way to inspect data in the
        ringbuffer in a continuous fashion.
        The price is that the data is copied into a newly allocated
        buffer.  For "raw" non-copy inspection of the data in the
        ringbuffer use `read_buffers`.

        Parameters
        ----------
        size : int
            Number of bytes to peek.

        Returns
        -------
        buffer
            A buffer object containing the requested data.
            If no more data is left (see `read_space`), a smaller
            (or even empty) buffer is returned.

        See Also
        --------
        read, :attr:`read_space`, :attr:`read_buffers`
        """
        ...
    @property
    def read_buffers(self) -> tuple[_CBufferType, _CBufferType]:
        """
        Contains two buffer objects that can be read directly.

        Two are needed because the data to be read may be split across
        the end of the ringbuffer.  Either of them could be 0 length.

        This can be used as a no-copy version of `peek()` or `read()`.

        When finished with reading, `read_advance()` should be used.

        .. note:: After an operation that changes the read pointer
           (`read()`, `read_advance()`, `reset()`), the buffers are no
           longer valid and one should use this property again to get
           new ones.
        """
        ...
    def read_advance(self, size: int) -> None:
        """
        Advance the read pointer.

        After data has been read from the ringbuffer using
        `read_buffers` or `peek()`, use this method to advance the
        buffer pointers, making that space available for future write
        operations.

        Parameters
        ----------
        size : int
            The number of bytes to advance.
        """
        ...
    def mlock(self) -> None:
        """
        Lock a ringbuffer data block into memory.

        Uses the ``mlock()`` system call.  This prevents the
        ringbuffer's memory from being paged to the swap area.

        .. note:: This is not a realtime operation.
        """
        ...
    def reset(self, size: int | None = None) -> None:
        """
        Reset the read and write pointers, making an empty buffer.

        .. note:: This is not thread safe.

        Parameters
        ----------
        size : int, optional
            The new size for the ringbuffer.
            Must be less than allocated size.
        """
        ...
    @property
    def size(self) -> int:
        """
        The number of bytes in total used by the buffer.

        See Also
        --------
        :attr:`read_space`, :attr:`write_space`
        """
        ...

class Status:
    __slots__ = "_code"
    def __init__(self, code: int) -> None: ...
    @property
    def failure(self) -> bool:
        """Overall operation failed."""
        ...
    @property
    def invalid_option(self) -> bool:
        """The operation contained an invalid or unsupported option."""
        ...
    @property
    def name_not_unique(self) -> bool:
        """
        The desired client name was not unique.

        With the *use_exact_name* option of `Client`, this situation is
        fatal.  Otherwise, the name is modified by appending a dash and
        a two-digit number in the range "-01" to "-99".  `Client.name`
        will return the exact string that was used.  If the specified
        *name* plus these extra characters would be too long, the open
        fails instead.
        """
        ...
    @property
    def server_started(self) -> bool:
        """
        The JACK server was started for this `Client`.

        Otherwise, it was running already.
        """
        ...
    @property
    def server_failed(self) -> bool:
        """Unable to connect to the JACK server."""
        ...
    @property
    def server_error(self) -> bool:
        """Communication error with the JACK server."""
        ...
    @property
    def no_such_client(self) -> bool:
        """Requested client does not exist."""
        ...
    @property
    def load_failure(self) -> bool:
        """Unable to load internal client."""
        ...
    @property
    def init_failure(self) -> bool:
        """Unable to initialize client."""
        ...
    @property
    def shm_failure(self) -> bool:
        """Unable to access shared memory."""
        ...
    @property
    def version_error(self) -> bool:
        """Client's protocol version does not match."""
        ...
    @property
    def backend_error(self) -> bool:
        """Backend error."""
        ...
    @property
    def client_zombie(self) -> bool:
        """Client zombified failure."""
        ...

class TransportState:
    __slots__ = "_code"
    def __init__(self, code: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class CallbackExit(Exception):
    """
    To be raised in a callback function to signal failure.

    See Also
    --------
    :meth:`Client.set_process_callback`
    :meth:`Client.set_blocksize_callback`
    :meth:`Client.set_samplerate_callback`
    :meth:`Client.set_port_rename_callback`
    :meth:`Client.set_graph_order_callback`
    :meth:`Client.set_xrun_callback`
    """
    ...

def get_property(subject: int | str, key: str) -> tuple[bytes, str] | None:
    """
    Get a metadata property on *subject*.

    Parameters
    ----------
    subject : int or str
        The subject (UUID) to get the property from.
        UUIDs can be obtained with `Client.uuid`, `Port.uuid` and
        `Client.get_uuid_for_client_name()`.
    key : str
        The key of the property.

    Returns
    -------
    (bytes, str) or None
        A tuple containing the value of the property and the type of the
        property.  If *subject* doesn't have the property *key*,
        ``None`` is returned.

    See Also
    --------
    Client.set_property
    get_properties
    get_all_properties
    Client.remove_property
    Client.remove_properties
    Client.remove_all_properties
    Client.set_property_change_callback
    """
    ...
def get_properties(subject: int | str) -> dict[str, tuple[bytes, str]]:
    """
    Get all metadata properties of *subject*.

    Parameters
    ----------
    subject : int or str
        The subject (UUID) to get all properties of.
        UUIDs can be obtained with `Client.uuid`, `Port.uuid` and
        `Client.get_uuid_for_client_name()`.

    Returns
    -------
    dict
        A dictionary mapping property names to ``(value, type)`` tuples.

    See Also
    --------
    Client.set_property
    get_property
    get_all_properties
    Client.remove_property
    Client.remove_properties
    Client.remove_all_properties
    Client.set_property_change_callback
    """
    ...
def get_all_properties() -> dict[int, dict[str, tuple[bytes, str]]]:
    """
    Get all properties for all subjects with metadata.

    Returns
    -------
    dict
        A dictionary mapping UUIDs to nested dictionaries as returned by
        `get_properties()`.

    See Also
    --------
    Client.set_property
    get_property
    get_properties
    Client.remove_property
    Client.remove_properties
    Client.remove_all_properties
    Client.set_property_change_callback
    """
    ...
def position2dict(pos: _JackPositionT) -> dict[str, Any]:
    """Convert CFFI position struct to a dict."""
    ...
def version() -> tuple[int, int, int, int]:
    """Get tuple of major/minor/micro/protocol version."""
    ...
def version_string() -> str:
    """Get human-readable JACK version."""
    ...
def client_name_size() -> int:
    """
    Return the maximum number of characters in a JACK client name.

    This includes the final NULL character.  This value is a constant.
    """
    ...
def port_name_size() -> int:
    """
    Maximum length of port names.

    The maximum number of characters in a full JACK port name including
    the final NULL character.  This value is a constant.

    A port's full name contains the owning client name concatenated with
    a colon (:) followed by its short name and a NULL character.
    """
    ...
def set_error_function(callback: Callable[[str], object] | None = None) -> None:
    """
    Set the callback for error message display.

    Set it to ``None`` to restore the default error callback function
    (which prints the error message plus a newline to stderr).
    The *callback* function must have this signature::

        callback(message: str) -> None
    """
    ...
def set_info_function(callback: Callable[[str], object] | None = None) -> None:
    """
    Set the callback for info message display.

    Set it to ``None`` to restore default info callback function
    (which prints the info message plus a newline to stderr).
    The *callback* function must have this signature::

        callback(message: str) -> None
    """
    ...
def client_pid(name: str) -> int:
    """
    Return PID of a JACK client.

    Parameters
    ----------
    name : str
        Name of the JACK client whose PID shall be returned.

    Returns
    -------
    int
        PID of *name*.  If not available, 0 will be returned.
    """
    ...

# Some METADATA_ constants are not available on all systems.
METADATA_CONNECTED: Final[str]
METADATA_HARDWARE: Final[str]
METADATA_ICON_LARGE: Final[str]
METADATA_ICON_SMALL: Final[str]
METADATA_PORT_GROUP: Final[str]
METADATA_PRETTY_NAME: Final[str]
METADATA_EVENT_TYPES: Final[str]
METADATA_ICON_NAME: Final[str]
METADATA_ORDER: Final[str]
METADATA_SIGNAL_TYPE: Final[str]
