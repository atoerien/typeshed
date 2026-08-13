from _typeshed import Incomplete
from collections import deque
from collections.abc import Generator
from typing_extensions import Self

from kafka.future import Future

class KafkaConnection:
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    node_id: Incomplete
    net: Incomplete
    transport: Incomplete | None
    parser: Incomplete | None
    paused: set[Incomplete]
    connected: bool
    initializing: bool
    in_flight_requests: deque[tuple[Incomplete, ...]]
    broker_version_data: Incomplete
    def __init__(self, net, node_id=None, broker_version_data=None, **configs) -> None: ...
    @property
    def broker_version(self): ...
    @property
    def closed(self) -> bool: ...
    @property
    def init_future(self) -> Future: ...
    def __await__(self) -> Generator[Future, Incomplete, Self]: ...
    @property
    def close_future(self) -> Future: ...
    def send_request(self, request, request_timeout_ms=None) -> Future: ...
    def send_buffered(self) -> None: ...
    def data_received(self, data) -> None:
        """Called when some data is received."""
        ...
    def eof_received(self):
        """
        Called when the other end calls write_eof() or equivalent.

        If this returns a false value (including None), the transport
        will close itself.  If it returns a true value, closing the
        transport is up to the protocol.
        """
        ...
    def connection_lost(self, exc) -> None:
        """
        Called when the connection is lost or closed.

        The argument is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """
        ...
    def fail_in_flight_requests(self, error) -> None: ...
    def connection_made(self, transport) -> None:
        """
        Called when a connection is made.

        The argument is the transport representing the pipe connection.
        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        """
        ...
    def pause(self, v) -> None: ...
    def unpause(self, v) -> None: ...
    def pause_writing(self) -> None:
        """
        Called when the transport's buffer goes over the high-water mark.

        Pause and resume calls are paired -- pause_writing() is called
        once when the buffer goes strictly over the high-water mark
        (even if subsequent writes increases the buffer size even
        more), and eventually resume_writing() is called once when the
        buffer size reaches the low-water mark.

        Note that if the buffer size equals the high-water mark,
        pause_writing() is not called -- it must go strictly over.
        Conversely, resume_writing() is called when the buffer size is
        equal or lower than the low-water mark.  These end conditions
        are important to ensure that things go as expected when either
        mark is zero.

        NOTE: This is the only Protocol callback that is not called
        through EventLoop.call_soon() -- if it were, it would have no
        effect when it's most needed (when the app keeps writing
        without yielding until pause_writing() is called).
        """
        ...
    def resume_writing(self) -> None:
        """Called when the transport's buffer drains below the low-water mark."""
        ...
    def close(self, error=None) -> None: ...
    async def initialize(self, timeout_at: float | None = None) -> None: ...
    @property
    def sasl_enabled(self) -> bool: ...

class SaslReauthenticator:
    """
    KIP-368 SASL re-authentication state and scheduling for a single
    KafkaConnection. Owns the per-connection re-auth lifecycle so the
    connection doesn't have to carry the related attributes and coroutines
    inline. The connection plugs this in at five points:

      - after each successful SASL auth                  -> session_updated()
      - after init completes                             -> schedule()
      - when send_request needs to gate the public API   -> is_reauthenticating
      - on every response popped from in_flight_requests -> on_response_processed()
      - on connection_lost                               -> cancel()
    """
    session_lifetime_ms: Incomplete
    authenticated_at: float | None
    def __init__(self, conn) -> None: ...
    @property
    def is_reauthenticating(self) -> bool: ...
    @property
    def task(self):
        """The scheduled re-auth task, or None. Exposed for tests/observability."""
        ...
    def session_updated(self, session_lifetime_ms) -> None:
        """
        Capture broker-advertised session lifetime after each successful
        auth round (initial and subsequent re-auths). Clamp negative values to 0,
        and require minimum non-zero lifetime of 1sec (1000).
        """
        ...
    def schedule(self) -> None:
        """
        Schedule the next re-auth before the lifetime elapses. Jittered to
        85-95% of the lifetime to avoid synchronised re-auth storms across
        many connections (Apache Java semantics). No-op when SASL is disabled
        or the broker advertised lifetime=0.
        """
        ...
    def cancel(self) -> None:
        """
        Cancel any pending re-auth and fail the drain awaiter if present.
        Called from KafkaConnection.connection_lost.
        """
        ...
    def on_response_processed(self) -> None:
        """
        Wake the drain awaiter once in_flight_requests clears during reauth.
        Called from KafkaConnection.data_received after each pop.
        """
        ...
