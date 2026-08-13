import abc
from _typeshed import Incomplete
from enum import IntEnum

from kafka.structs import OffsetAndMetadata
from kafka.util import synchronized

class SubscriptionType(IntEnum):
    """An enumeration."""
    NONE = 0
    AUTO_TOPICS = 1
    AUTO_PATTERN = 2
    USER_ASSIGNED = 3

class SubscriptionState:
    """
    A class for tracking the topics, partitions, and offsets for the consumer.
    A partition is "assigned" either directly with assign_from_user() (manual
    assignment) or with assign_from_subscribed() (automatic assignment from
    subscription).

    Once assigned, the partition is not considered "fetchable" until its initial
    position has been set with seek(). Fetchable partitions track a fetch
    position which is used to set the offset of the next fetch, and a consumed
    position which is the last offset that has been returned to the user. You
    can suspend fetching from a partition through pause() without affecting the
    fetched/consumed offsets. The partition will remain unfetchable until the
    resume() is used. You can also query the pause state independently with
    is_paused().

    Note that pause state as well as fetch/consumed positions are not preserved
    when partition assignment is changed whether directly by the user or
    through a group rebalance.
    """
    subscription: Incomplete
    subscription_type: Incomplete
    subscribed_pattern: Incomplete
    assignment: Incomplete
    rebalance_listener: Incomplete
    listeners: Incomplete
    def __init__(self, offset_reset_strategy: str = "earliest") -> None:
        """
        Initialize a SubscriptionState instance

        Keyword Arguments:
            offset_reset_strategy: 'earliest' or 'latest', otherwise
                exception will be raised when fetching an offset that is no
                longer available. Default: 'earliest'
        """
        ...
    @synchronized
    def subscribe(self, topics=(), pattern=None, listener=None) -> None:
        """
        Subscribe to a list of topics, or a topic regex pattern.

        Partitions will be dynamically assigned via a group coordinator.
        Topic subscriptions are not incremental: this list will replace the
        current assignment (if there is one).

        This method is incompatible with assign_from_user()

        Arguments:
            topics (list): List of topics for subscription.
            pattern (str): Pattern to match available topics. You must provide
                either topics or pattern, but not both.
            listener (ConsumerRebalanceListener): Optionally include listener
                callback, which will be called before and after each rebalance
                operation.

                As part of group management, the consumer will keep track of the
                list of consumers that belong to a particular group and will
                trigger a rebalance operation if one of the following events
                trigger:

                * Number of partitions change for any of the subscribed topics
                * Topic is created or deleted
                * An existing member of the consumer group dies
                * A new member is added to the consumer group

                When any of these events are triggered, the provided listener
                will be invoked first to indicate that the consumer's assignment
                has been revoked, and then again when the new assignment has
                been received. Note that this listener will immediately override
                any listener set in a previous call to subscribe. It is
                guaranteed, however, that the partitions revoked/assigned
                through this interface are from topics subscribed in this call.

        Raises:
            ValueError: if neither topics nor pattern provided.
            IllegalStateError: if both topics and pattern provided.
            TypeError: if topics is not a list/sequence, or listener is not
                a AsyncConsumerRebalanceListener or ConsumerRebalanceListener.
        """
        ...
    @synchronized
    def change_subscription(self, topics) -> None:
        """
        Change the topic subscription.

        Arguments:
            topics (list of str): topics for subscription

        Raises:
            IllegalStateError: if assign_from_user has been used already
            TypeError: if a topic is None or a non-str
            ValueError: if a topic is an empty string or
                        - a topic name is '.' or '..' or
                        - a topic name does not consist of ASCII-characters/'-'/'_'/'.'
        """
        ...
    @synchronized
    def group_subscribe(self, topics) -> None:
        """
        Add topics to the current group subscription.

        This is used by the group leader to ensure that it receives metadata
        updates for all topics that any member of the group is subscribed to.

        Arguments:
            topics (list of str): topics to add to the group subscription
        """
        ...
    @synchronized
    def reset_group_subscription(self) -> None:
        """Reset the group's subscription to only contain topics subscribed by this consumer."""
        ...
    @synchronized
    def assign_from_user(self, partitions) -> None:
        """
        Manually assign a list of TopicPartitions to this consumer.

        The new assignment replaces the previous one (this is not an
        incremental-add API), but ``TopicPartitionState`` is preserved
        for any partition that's present in both the old and new
        assignment. Manual topic assignment through this method does
        not use the consumer's group management functionality. As
        such, there will be no rebalance operation triggered when
        group membership or cluster and topic metadata change. Note
        that it is not possible to use both manual partition
        assignment with assign() and group assignment with subscribe().

        Arguments:
            partitions (list of TopicPartition): assignment for this instance.

        Raises:
            IllegalStateError: if consumer has already called subscribe()
        """
        ...
    @synchronized
    def assign_from_subscribed(self, assignments) -> None:
        """
        Update the assignment to the specified partitions.

        This method is called by the coordinator to dynamically assign
        partitions based on the consumer's topic subscription. Differs
        from :meth:`assign_from_user` which directly sets the assignment
        from a user-supplied TopicPartition list.

        Preserves ``TopicPartitionState`` (position, paused flag,
        preferred read replica, fetch buffers tied to the partition)
        for any partition present in both the prior and new assignments.

        Validation raises ``ValueError`` BEFORE any mutation if a
        partition's topic isn't subscribed.

        Arguments:
            assignments (list of TopicPartition): the *full* new
                assignment (not a diff). Partitions present in both
                the old and new assignment retain their state;
                revoked partitions are dropped; new partitions get
                fresh state.
        """
        ...
    @synchronized
    def unsubscribe(self) -> None:
        """Clear all topic subscriptions and partition assignments"""
        ...
    @synchronized
    def group_subscription(self):
        """
        Get the topic subscription for the group.

        For the leader, this will include the union of all member subscriptions.
        For followers, it is the member's subscription only.

        This is used when querying topic metadata to detect metadata changes
        that would require rebalancing (the leader fetches metadata for all
        topics in the group so that it can do partition assignment).

        Returns:
            set: topics
        """
        ...
    @synchronized
    def seek(self, partition, offset) -> None:
        """
        Manually specify the fetch offset for a TopicPartition.

        Overrides the fetch offsets that the consumer will use on the next
        poll(). If this API is invoked for the same partition more than once,
        the latest offset will be used on the next poll(). Note that you may
        lose data if this API is arbitrarily used in the middle of consumption,
        to reset the fetch offsets.

        Arguments:
            partition (TopicPartition): partition for seek operation
            offset (int or OffsetAndMetadata): message offset in partition
        """
        ...
    @synchronized
    def assigned_partitions(self):
        """Return set of TopicPartitions in current assignment."""
        ...
    @synchronized
    def paused_partitions(self):
        """Return current set of paused TopicPartitions."""
        ...
    @synchronized
    def fetchable_partitions(self):
        """Return ordered list of TopicPartitions that should be Fetched."""
        ...
    @synchronized
    def partitions_auto_assigned(self):
        """Return True unless user supplied partitions manually."""
        ...
    @synchronized
    def all_consumed_offsets(self):
        """Returns consumed offsets as {TopicPartition: OffsetAndMetadata}"""
        ...
    @synchronized
    def request_offset_reset(self, partition, offset_reset_strategy=None) -> None:
        """
        Mark partition for offset reset using specified or default strategy.

        Arguments:
            partition (TopicPartition): partition to mark
            offset_reset_strategy (OffsetResetStrategy, optional)
        """
        ...
    @synchronized
    def set_reset_pending(self, partitions, next_allowed_reset_time) -> None: ...
    @synchronized
    def has_default_offset_reset_policy(self):
        """Return True if default offset reset policy is Earliest or Latest"""
        ...
    @synchronized
    def is_offset_reset_needed(self, partition): ...
    @synchronized
    def has_all_fetch_positions(self): ...
    @synchronized
    def missing_fetch_positions(self): ...
    @synchronized
    def has_valid_position(self, partition): ...
    @synchronized
    def reset_missing_positions(self) -> None: ...
    @synchronized
    def partitions_needing_reset(self): ...
    @synchronized
    def next_offset_reset_retry_time(self): ...
    @synchronized
    def maybe_validate_position_for_current_leader(self, partition, current_leader_epoch) -> bool: ...
    @synchronized
    def request_position_validation(self, partition) -> bool: ...
    @synchronized
    def partitions_needing_validation(self) -> set[Incomplete]: ...
    @synchronized
    def next_offset_validation_retry_time(self): ...
    @synchronized
    def set_validation_pending(self, partitions, next_allowed_retry_time) -> None: ...
    @synchronized
    def validation_failed(self, partitions, next_allowed_retry_time) -> None: ...
    @synchronized
    def complete_validation(self, partition, validated_position=None) -> None: ...
    @synchronized
    def is_offset_validation_needed(self, partition) -> bool: ...
    @synchronized
    def is_assigned(self, partition) -> bool: ...
    @synchronized
    def is_paused(self, partition): ...
    @synchronized
    def is_fetchable(self, partition) -> bool: ...
    @synchronized
    def pause(self, partition) -> None: ...
    @synchronized
    def resume(self, partition) -> None: ...
    @synchronized
    def mark_pending_revocation(self, partitions) -> None:
        """
        KIP-429: gate ``is_fetchable()`` for each partition's state
        so the fetcher would skip them while an on_partitions_revoked /
        on_partitions_lost listener runs. Called immediately before
        invoking the listener. The flag is single-shot - the
        surrounding ``assign_from_subscribed`` drops the
        ``TopicPartitionState`` for revoked partitions when the
        listener returns.

        Currently a no-op while the user thread is blocked in ``_net.run``
        during rebalance and so the only path that calls ``send_fetches``
        cannot fire. Kept as a defensive gate in case this changes in
        the future.
        """
        ...
    @synchronized
    def reset_failed(self, partitions, next_retry_time) -> None: ...
    @synchronized
    def move_partition_to_end(self, partition) -> None: ...
    @synchronized
    def position(self, partition): ...

class TopicPartitionState:
    paused: bool
    reset_strategy: Incomplete
    highwater: Incomplete
    drop_pending_record_batch: bool
    next_allowed_retry_time: Incomplete
    def __init__(self) -> None: ...

    @property
    def position(self) -> OffsetAndMetadata | None:
        """last position"""
        ...
    @position.setter
    def position(self, offset: OffsetAndMetadata) -> None:
        """last position"""
        ...

    def reset(self, strategy) -> None: ...
    def is_reset_allowed(self) -> bool: ...
    @property
    def awaiting_reset(self) -> bool: ...
    def set_reset_pending(self, next_allowed_retry_time) -> None: ...
    def reset_failed(self, next_allowed_retry_time) -> None: ...
    @property
    def has_valid_position(self) -> bool: ...
    def is_missing_position(self) -> bool: ...
    def seek(self, offset) -> None: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def mark_pending_revocation(self, val: bool = True) -> None:
        """
        KIP-429: gate fetches while an on_partitions_revoked /
        on_partitions_lost listener is in progress for this partition.
        Single-shot: the surrounding ``assign_from_subscribed`` drops
        the state object once the listener returns.
        """
        ...
    def is_fetchable(self) -> bool: ...
    def preferred_read_replica(self):
        """
        Return the currently-cached preferred read replica (KIP-392),
        or None if unset/expired. Lazily clears the cache on expiry.
        """
        ...
    def update_preferred_read_replica(self, node_id, expiration_time) -> bool:
        """
        Cache the broker's chosen preferred read replica until ``expiration_time``
        (monotonic). ``node_id == -1`` (or None) clears the cache.

        Returns True if the cached replica actually changed (caller can log).
        """
        ...
    def clear_preferred_read_replica(self):
        """
        Clear the cached preferred read replica. Returns the previously-
        cached node_id (or None) so the caller can log the eviction.
        """
        ...
    @property
    def awaiting_validation(self) -> bool: ...
    def maybe_validate_position(self, current_leader_epoch) -> bool:
        """
        Mark for validation if the current leader has advanced beyond the
        leader epoch this position was last reconciled against.

        Returns True if the partition is now awaiting validation.
        """
        ...
    def request_position_validation(self) -> bool:
        """Force validation (e.g., after FENCED/UNKNOWN epoch errors from the broker)."""
        ...
    def is_validation_allowed(self) -> bool: ...
    def set_validation_pending(self, next_allowed_retry_time) -> None: ...
    def validation_failed(self, next_allowed_retry_time) -> None: ...
    def complete_validation(self, validated_position=None) -> None: ...

class ConsumerRebalanceListener(metaclass=abc.ABCMeta):
    """
    A callback interface that the user can implement to trigger custom actions
    when the set of partitions assigned to the consumer changes.

    This is applicable when the consumer is having Kafka auto-manage group
    membership. If the consumer's directly assign partitions, those
    partitions will never be reassigned and this callback is not applicable.

    When Kafka is managing the group membership, a partition re-assignment will
    be triggered any time the members of the group changes or the subscription
    of the members changes. This can occur when processes die, new process
    instances are added or old instances come back to life after failure.
    Rebalances can also be triggered by changes affecting the subscribed
    topics (e.g. when then number of partitions is administratively adjusted).

    There are many uses for this functionality. One common use is saving offsets
    in a custom store. By saving offsets in the on_partitions_revoked(), call we
    can ensure that any time partition assignment changes the offset gets saved.

    Another use is flushing out any kind of cache of intermediate results the
    consumer may be keeping. For example, consider a case where the consumer is
    subscribed to a topic containing user page views, and the goal is to count
    the number of page views per users for each five minute window.  Let's say
    the topic is partitioned by the user id so that all events for a particular
    user will go to a single consumer instance. The consumer can keep in memory
    a running tally of actions per user and only flush these out to a remote
    data store when its cache gets too big. However if a partition is reassigned
    it may want to automatically trigger a flush of this cache, before the new
    owner takes over consumption.

    Threading: callbacks run on the consumer's IO event loop, the same loop
    that drives heartbeats. Sync listener methods must return promptly --
    blocking IO inside a sync listener will block heartbeats for the duration
    and can cause the consumer to be kicked from the group if the listener
    runs longer than ``session_timeout_ms``. For listeners that need to do
    blocking work (e.g. flushing state to a database), prefer
    :class:`AsyncConsumerRebalanceListener`, which lets you ``await`` while
    keeping the loop responsive, or wrap the blocking call in your own
    worker thread.

    It is guaranteed that all consumer processes will invoke
    on_partitions_revoked() prior to any process invoking
    on_partitions_assigned(). So if offsets or other state is saved in the
    on_partitions_revoked() call, it should be saved by the time the process
    taking over that partition has their on_partitions_assigned() callback
    called to load the state.
    """
    @abc.abstractmethod
    def on_partitions_revoked(self, revoked):
        """
        A callback method the user can implement to provide handling of offset
        commits to a customized store on the start of a rebalance operation.
        This method will be called before a rebalance operation starts and
        after the consumer stops fetching data. It is recommended that offsets
        should be committed in this callback to either Kafka or a custom offset
        store to prevent duplicate data.

        NOTE: This method is called before each rebalance and also when the
        consumer is closing (KafkaConsumer.close()), so that offsets / state
        can be committed before the partitions are given up. If the group
        membership has already been lost (forced eviction),
        on_partitions_lost() is called instead.

        Arguments:
            revoked (list of TopicPartition): the partitions that were assigned
                to the consumer on the last rebalance
        """
        ...
    @abc.abstractmethod
    def on_partitions_assigned(self, assigned):
        """
        A callback method the user can implement to provide handling of
        customized offsets on completion of a successful partition
        re-assignment. This method will be called after an offset re-assignment
        completes and before the consumer starts fetching data.

        It is guaranteed that all the processes in a consumer group will execute
        their on_partitions_revoked() callback before any instance executes its
        on_partitions_assigned() callback.

        Arguments:
            assigned (list of TopicPartition): the partitions assigned to the
                consumer (may include partitions that were previously assigned)
        """
        ...
    def on_partitions_lost(self, lost):
        """
        KIP-429: called when the consumer has been forcibly removed
        from the group (heartbeat session expiry, ``UnknownMemberIdError``,
        ``IllegalGenerationError``, ``FencedInstanceIdError``) and the
        partitions cannot be cleanly committed. ``on_partitions_revoked``
        implies the user *can* still commit; ``on_partitions_lost`` makes
        explicit that the member has been booted and any in-flight state
        for these partitions should be discarded.

        Default behaviour is to delegate to ``on_partitions_revoked`` so
        listeners written before KIP-429 keep working unchanged. Override
        for cleanup that is specific to the forced-eviction case (e.g.
        skipping a commit attempt that will fail anyway).

        Arguments:
            lost (set of TopicPartition): the partitions that were
                assigned but have been lost due to forced eviction.
        """
        ...

class AsyncConsumerRebalanceListener(metaclass=abc.ABCMeta):
    """
    Async variant of :class:`ConsumerRebalanceListener`.

    Implement this when your rebalance hooks need to perform IO that would
    otherwise block the consumer's event loop -- e.g. flushing state to a
    database, calling an external service, or coordinating with other async
    code. The coordinator detects coroutine functions and ``await`` s them
    instead of calling inline, so other tasks on the loop (notably the
    heartbeat coroutine) continue to run while your listener is suspended.

    Same lifecycle and ordering guarantees as the sync listener: all
    consumers in the group invoke ``on_partitions_revoked`` before any
    invokes ``on_partitions_assigned``. Both methods must be defined as
    ``async def``; otherwise use :class:`ConsumerRebalanceListener`.
    """
    @abc.abstractmethod
    async def on_partitions_revoked(self, revoked):
        """
        Async-callback for the start of a rebalance operation.

        See :meth:`ConsumerRebalanceListener.on_partitions_revoked` for
        semantics. The coordinator awaits this method, so non-blocking IO
        via ``await`` keeps the heartbeat loop responsive during the call.

        Arguments:
            revoked (set of TopicPartition): the partitions that were
                assigned to the consumer on the last rebalance.
        """
        ...
    @abc.abstractmethod
    async def on_partitions_assigned(self, assigned):
        """
        Async-callback for the completion of a partition re-assignment.

        See :meth:`ConsumerRebalanceListener.on_partitions_assigned` for
        semantics.

        Arguments:
            assigned (set of TopicPartition): the partitions assigned to
                the consumer (may include partitions that were previously
                assigned).
        """
        ...
    async def on_partitions_lost(self, lost):
        """
        Async variant of
        :meth:`ConsumerRebalanceListener.on_partitions_lost`. Default
        implementation awaits ``on_partitions_revoked`` for backward
        compatibility with listeners written before KIP-429.

        Arguments:
            lost (set of TopicPartition): the partitions that were
                assigned but have been lost due to forced eviction.
        """
        ...
