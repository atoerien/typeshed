import abc
from _typeshed import Incomplete
from typing import ClassVar, Final
from typing_extensions import deprecated

from kafka import errors as Errors
from kafka.structs import ConsumerGroupMetadata

class Generation:
    NO_GENERATION: ClassVar[Generation]
    generation_id: Incomplete
    member_id: Incomplete
    protocol: Incomplete
    def __init__(self, generation_id, member_id, protocol) -> None: ...
    def has_member_id(self) -> bool: ...
    def is_lost(self) -> bool: ...
    def __eq__(self, other) -> bool: ...

class UnjoinedGroupException(Errors.KafkaError): ...

class BaseCoordinator(metaclass=abc.ABCMeta):
    """
    BaseCoordinator implements group management for a single group member
    by interacting with a designated Kafka broker (the coordinator). Group
    semantics are provided by extending this class.  See ConsumerCoordinator
    for example usage.

    From a high level, Kafka's group management protocol consists of the
    following sequence of actions:

    1. Group Registration: Group members register with the coordinator providing
       their own metadata (such as the set of topics they are interested in).

    2. Group/Leader Selection: The coordinator select the members of the group
       and chooses one member as the leader.

    3. State Assignment: The leader collects the metadata from all the members
       of the group and assigns state.

    4. Group Stabilization: Each member receives the state assigned by the
       leader and begins processing.

    To leverage this protocol, an implementation must define the format of
    metadata provided by each member for group registration in
    :meth:`.group_protocols` and the format of the state assignment provided by
    the leader in :meth:`._perform_assignment` and which becomes available to
    members in :meth:`._on_join_complete`.

    Note on locking: this class shares state between the caller and a background
    thread which is used for sending heartbeats after the client has joined the
    group. All mutable state as well as state transitions are protected with the
    class's monitor. Generally this means acquiring the lock before reading or
    writing the state of the group (e.g. generation, member_id) and holding the
    lock when sending a request that affects the state of the group
    (e.g. JoinGroup, LeaveGroup).
    """
    DEFAULT_CONFIG: Incomplete
    config: Incomplete
    heartbeat: Incomplete
    rejoin_needed: bool
    rejoining: bool
    state: Incomplete
    coordinator_id: Incomplete
    DEFAULT_SESSION_TIMEOUT_MS_PRE_KIP_735: Final = 30000
    def __init__(self, client, **configs) -> None: ...
    @property
    def group_id(self): ...
    @property
    def group_instance_id(self): ...
    @abc.abstractmethod
    def protocol_type(self):
        """
        Unique identifier for the class of supported protocols
        (e.g. "consumer" or "connect").

        Returns:
            str: protocol type name
        """
        ...
    @abc.abstractmethod
    def group_protocols(self): ...
    def coordinator_unknown(self): ...
    def coordinator(self): ...
    def stable(self) -> bool: ...
    def ensure_coordinator_ready(self, timeout_ms=None) -> bool: ...
    async def ensure_coordinator_ready_async(self, timeout_ms=None) -> bool: ...
    def lookup_coordinator(self): ...
    def need_rejoin(self): ...
    def poll_heartbeat(self) -> None: ...
    def time_to_next_heartbeat(self): ...
    def ensure_active_group(self, timeout_ms=None) -> bool: ...
    async def ensure_active_group_async(self, timeout_ms=None) -> bool: ...
    async def join_group_async(self, timeout_ms=None) -> bool: ...
    def coordinator_dead(self, error) -> None: ...
    def generation_if_stable(self): ...
    def group_metadata(self) -> ConsumerGroupMetadata: ...
    @deprecated("Deprecated. Use `coordinator.generation_if_stable()` instead.")
    def generation(self): ...
    def rebalance_in_progress(self): ...
    def reset_generation(self, member_id="") -> None:
        """Reset the generation and member_id because we have fallen out of the group."""
        ...
    def request_rejoin(self) -> None: ...
    def close(self, timeout_ms=None) -> None: ...
    def is_dynamic_member(self): ...
    def maybe_leave_group(self, reason=None, timeout_ms=None) -> None: ...
    async def maybe_leave_group_async(self, reason=None, timeout_ms=None) -> None: ...

class GroupCoordinatorMetrics:
    heartbeat: Incomplete
    metrics: Incomplete
    metric_group_name: Incomplete
    heartbeat_latency: Incomplete
    join_latency: Incomplete
    sync_latency: Incomplete
    def __init__(self, heartbeat, metrics, prefix, tags=None) -> None: ...
