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
    def has_member_id(self) -> bool:
        """
        True if this generation has a valid member id, False otherwise.
        A member might have an id before it becomes part of a group generation.
        """
        ...
    def is_lost(self) -> bool:
        """
        True if this generation is effectively the no-generation
        sentinel - either the generation_id has been cleared
        (DEFAULT_GENERATION_ID) or the member_id has been cleared
        (UNKNOWN_MEMBER_ID). Mirrors Java's NO_GENERATION-or-empty-memberId
        check in ConsumerCoordinator.onJoinPrepare; used to fire
        on_partitions_lost (KIP-429) instead of on_partitions_revoked
        when the broker has forcibly removed us from the group.
        """
        ...
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
    def __init__(self, client, **configs) -> None:
        """
        Keyword Arguments:
            group_id (str): name of the consumer group to join for dynamic
                partition assignment (if enabled), and to use for fetching and
                committing offsets. Default: 'kafka-python-default-group'
            group_instance_id (str): A unique identifier of the consumer instance
                provided by end user. Only non-empty strings are permitted. If set,
                the consumer is treated as a static member, which means that only
                one instance with this ID is allowed in the consumer group at any
                time. This can be used in combination with a larger session timeout
                to avoid group rebalances caused by transient unavailability (e.g.
                process restarts). If not set, the consumer will join the group as
                a dynamic member, which is the traditional behavior. Default: None
            session_timeout_ms (int): The timeout used to detect failures when
                using Kafka's group management facilities. The consumer sends
                periodic heartbeats to indicate its liveness to the broker. If
                no heartbeats are received by the broker before the expiration of
                this session timeout, then the broker will remove this consumer
                from the group and initiate a rebalance. Note that the value must
                be in the allowable range as configured in the broker configuration
                by group.min.session.timeout.ms and group.max.session.timeout.ms.
                Default: 45000 for brokers 3.0+, otherwise 30000.
            heartbeat_interval_ms (int): The expected time in milliseconds
                between heartbeats to the consumer coordinator when using
                Kafka's group management feature. Heartbeats are used to ensure
                that the consumer's session stays active and to facilitate
                rebalancing when new consumers join or leave the group. The
                value must be set lower than session_timeout_ms, but typically
                should be set no higher than 1/3 of that value. It can be
                adjusted even lower to control the expected time for normal
                rebalances. Default: 3000
            retry_backoff_ms (int): Milliseconds to backoff when retrying on
                errors. Default: 100.
        """
        ...
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
    def group_protocols(self):
        """
        Return the list of supported group protocols and metadata.

        This list is submitted by each group member via a JoinGroupRequest.
        The order of the protocols in the list indicates the preference of the
        protocol (the first entry is the most preferred). The coordinator takes
        this preference into account when selecting the generation protocol
        (generally more preferred protocols will be selected as long as all
        members support them and there is no disagreement on the preference).

        Note: metadata must be type bytes or support an encode() method

        Returns:
            list: [(protocol, metadata), ...]
        """
        ...
    def coordinator_unknown(self):
        """
        Check if we know who the coordinator is and have an active connection

        Side-effect: reset coordinator_id to None if connection failed

        Returns:
            bool: True if the coordinator is unknown
        """
        ...
    def coordinator(self):
        """
        Get the current coordinator

        Returns: the current coordinator id or None if it is unknown
        """
        ...
    def stable(self) -> bool: ...
    def ensure_coordinator_ready(self, timeout_ms=None) -> bool:
        """
        Block until the coordinator for this group is known.

        Keyword Arguments:
            timeout_ms (numeric, optional): Maximum number of milliseconds to
                block waiting to find coordinator. Default: None.

        Returns: True is coordinator found before timeout_ms, else False
        """
        ...
    async def ensure_coordinator_ready_async(self, timeout_ms=None) -> bool:
        """
        Async variant of :meth:`ensure_coordinator_ready`.

        Awaits until the coordinator for this group is known, or until the
        timeout (if any) expires.
        """
        ...
    def lookup_coordinator(self): ...
    def need_rejoin(self):
        """
        Check whether the group should be rejoined (e.g. if metadata changes)

        Returns:
            bool: True if it should, False otherwise
        """
        ...
    def poll_heartbeat(self) -> None:
        """
        Check the status of the heartbeat coroutine and indicate the liveness
        of the client. This must be called periodically after joining with
        :meth:`.ensure_active_group` to ensure that the member stays in the
        group. If an interval of time longer than the provided rebalance
        timeout (max_poll_interval_ms) expires without calling this method,
        then the client will proactively leave the group.

        Raises: the underlying exception if the heartbeat coroutine has
        terminated with an error. The next call to ensure_active_group will
        respawn the loop.
        """
        ...
    def time_to_next_heartbeat(self):
        """
        Returns seconds (float) remaining before next heartbeat should be sent

        Note: Returns infinite if group is not joined
        """
        ...
    def ensure_active_group(self, timeout_ms=None) -> bool:
        """
        Ensure that the group is active (i.e. joined and synced).

        Sync facade over :meth:`ensure_active_group_async`.

        Keyword Arguments:
            timeout_ms (numeric, optional): Maximum number of milliseconds to
                block waiting to join group. Default: None.

        Returns: True if group initialized before timeout_ms, else False
        """
        ...
    async def ensure_active_group_async(self, timeout_ms=None) -> bool:
        """Async variant of :meth:`ensure_active_group`."""
        ...
    async def join_group_async(self, timeout_ms=None) -> bool:
        """
        Drive JoinGroup -> SyncGroup attempts until joined or aborted.

        Internal: the only entry point is :meth:`ensure_active_group_async`
        (and its sync facade :meth:`ensure_active_group`).

        Returns True when the member has been (re-)joined, False on timer
        expiry, or raises on a non-retriable error.
        """
        ...
    def coordinator_dead(self, error) -> None:
        """Mark the current coordinator as dead."""
        ...
    def generation_if_stable(self):
        """
        Get the current generation state if the group is stable.

        Returns: the current generation or None if the group is unjoined/rebalancing
        """
        ...
    def group_metadata(self) -> ConsumerGroupMetadata:
        """
        Return a snapshot of this member's group membership.

        Returns the current generation_id / member_id / group_instance_id even
        when the group is not stable; the caller (typically
        KafkaProducer.send_offsets_to_transaction) needs whatever is current
        so the broker can fence stale instances (KIP-447). If the consumer has
        never joined, the snapshot has the no-generation defaults.

        Also carries the live MemberState (``state``) so callers can observe
        whether the group has converged (it is ignored by the fencing path).
        """
        ...
    @deprecated("Deprecated. Use `coordinator.generation_if_stable()` instead.")
    def generation(self): ...
    def rebalance_in_progress(self): ...
    def reset_generation(self, member_id="") -> None:
        """
        Reset the generation and member_id because we have fallen out of the group.

        Arguments:
            member_id (str): new local member id to record. Defaults to
                ``UNKNOWN_MEMBER_ID``. The broker hands back a real member id
                on a ``MemberIdRequiredError`` retry; that path passes the
                broker-returned id through here.
        """
        ...
    def request_rejoin(self) -> None: ...
    def close(self, timeout_ms=None) -> None:
        """
        Close the coordinator, leave the current group,
        and reset local generation / member_id
        """
        ...
    def is_dynamic_member(self): ...
    def maybe_leave_group(self, reason=None, timeout_ms=None) -> None:
        """Leave the current group and reset local generation/member_id."""
        ...
    async def maybe_leave_group_async(self, reason=None, timeout_ms=None) -> None: ...

class GroupCoordinatorMetrics:
    heartbeat: Incomplete
    metrics: Incomplete
    metric_group_name: Incomplete
    heartbeat_latency: Incomplete
    join_latency: Incomplete
    sync_latency: Incomplete
    def __init__(self, heartbeat, metrics, prefix, tags=None) -> None: ...
