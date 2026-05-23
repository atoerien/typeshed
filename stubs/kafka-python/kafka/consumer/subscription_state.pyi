import abc
from _typeshed import Incomplete
from enum import IntEnum

from kafka.util import synchronized

log: Incomplete

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

        This interface does not allow for incremental assignment and will
        replace the previous assignment (if there was one).

        Manual topic assignment through this method does not use the consumer's
        group management functionality. As such, there will be no rebalance
        operation triggered when group membership or cluster and topic metadata
        change. Note that it is not possible to use both manual partition
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
        Update the assignment to the specified partitions

        This method is called by the coordinator to dynamically assign
        partitions based on the consumer's topic subscription. This is different
        from assign_from_user() which directly sets the assignment from a
        user-supplied TopicPartition list.

        Arguments:
            assignments (list of TopicPartition): partitions to assign to this
                consumer instance.
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
    def is_assigned(self, partition): ...
    @synchronized
    def is_paused(self, partition): ...
    @synchronized
    def is_fetchable(self, partition): ...
    @synchronized
    def pause(self, partition) -> None: ...
    @synchronized
    def resume(self, partition) -> None: ...
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
    position: Incomplete
    def reset(self, strategy) -> None: ...
    def is_reset_allowed(self): ...
    @property
    def awaiting_reset(self): ...
    def set_reset_pending(self, next_allowed_retry_time) -> None: ...
    def reset_failed(self, next_allowed_retry_time) -> None: ...
    @property
    def has_valid_position(self): ...
    def is_missing_position(self): ...
    def seek(self, offset) -> None: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def is_fetchable(self): ...

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

    This callback will execute in the user thread as part of the Consumer.poll()
    whenever partition assignment changes.

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

        NOTE: This method is only called before rebalances. It is not called
        prior to KafkaConsumer.close()

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
