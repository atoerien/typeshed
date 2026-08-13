from _typeshed import Incomplete

from kafka.cluster import ClusterMetadata
from kafka.future import Future
from kafka.protocol.broker_version_data import BrokerVersionData

class KafkaConnectionManager:
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    cluster: ClusterMetadata
    broker_version_data: BrokerVersionData | None
    closed: bool
    def __init__(self, net, **configs) -> None: ...
    @property
    def broker_version(self): ...
    def least_used_connections(self) -> list[Incomplete]: ...
    def bootstrap_async(self, timeout_ms=None, refresh: bool = True): ...
    def bootstrap(self, timeout_ms=None, refresh: bool = True) -> None: ...
    @property
    def bootstrapped(self) -> bool: ...
    def close_idle_connections(self) -> None: ...
    @property
    def ssl_enabled(self) -> bool: ...
    def get_connection(
        self,
        node_id,
        timeout_ms=None,
        pop_on_close: bool = True,
        refresh_metadata_on_err: bool = True,
        reset_backoff_on_connect: bool = True,
    ): ...
    def send(self, request, node_id=None, request_timeout_ms=None): ...
    def least_loaded_node(self):
        """
        Choose the node with fewest outstanding requests, with fallbacks.

        This method will prefer a node with an existing connection (not throttled)
        with no in-flight-requests. If no such node is found, a node will be chosen
        randomly from all nodes that are not throttled or "blacked out" (i.e.,
        are not subject to a reconnect backoff). If no node metadata has been
        obtained, will return a bootstrap node.

        Returns:
            node_id or None if no suitable node was found
        """
        ...
    def reset_backoff(self, node_id) -> None: ...
    def jitter_pct(self) -> float: ...
    def update_backoff(self, node_id): ...
    def connection_delay(self, node_id) -> int:
        """
        Connection delay in seconds.

        Uses exponential backoff/retry with jitter. See KIP-144.
        """
        ...
    def socket_connection_setup_timeout_ms(self, node_id): ...
    def auth_failure(self, node_id):
        """
        Return the most recent auth-class failure for ``node_id``,
        or None if there is no sticky failure on record.
        """
        ...
    def maybe_raise_auth_failure(self, node_id) -> None:
        """Raise the cached auth-class failure for ``node_id`` if any."""
        ...
    def close(self, node_id=None, timeout_ms=None) -> None: ...
    async def wait_for(self, future, timeout_ms):
        """
        Await `future` with a timeout in ms. Raises KafkaTimeoutError on timeout.

        Must be awaited from a coroutine running on this loop. The underlying
        future is not cancelled on timeout - it continues to run; the timeout
        only unblocks the awaiter.
        """
        ...
    def call_soon(self, coro, *args) -> Future:
        """
        Accepts a coroutine / awaitable / function and schedules it on the event loop.

        Thread-safe.

        Returns: Future
        """
        ...
    def run(self, coro, *args):
        """
        Schedules coro on the event loop, blocks until complete, returns value or raises.

        If an IO thread is running (via start()), the caller thread blocks on
        a cross-thread Event while the coroutine runs on the IO thread. Safe
        to call concurrently from multiple caller threads.

        If no IO thread is running, falls back to driving the loop on the
        caller thread (legacy behavior).
        """
        ...
