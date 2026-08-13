from _typeshed import Incomplete

from kafka.coordinator.base import BaseCoordinator

class ConsumerCoordinator(BaseCoordinator):
    """This class manages the coordination process with the consumer coordinator."""
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    auto_commit_interval: Incomplete
    next_auto_commit_deadline: Incomplete
    completed_offset_commits: Incomplete
    def __init__(self, client, subscription, **configs) -> None:
        """
        Initialize the coordination manager.

        Keyword Arguments:
            group_id (str): name of the consumer group to join for dynamic
                partition assignment (if enabled), and to use for fetching and
                committing offsets. Default: 'kafka-python-default-group'
            enable_auto_commit (bool): If true the consumer's offset will be
                periodically committed in the background. Default: True.
            auto_commit_interval_ms (int): milliseconds between automatic
                offset commits, if enable_auto_commit is True. Default: 5000.
            default_offset_commit_callback (callable): called as
                callback(offsets, response) response will be either an Exception
                or None. This callback can be used to trigger custom actions when
                a commit request completes.
            assignors (list): List of objects to use to distribute partition
                ownership amongst consumer instances when group management is
                used. Default: [RangePartitionAssignor, RoundRobinPartitionAssignor, StickyPartitionAssignor]
            retry_backoff_ms (int): Milliseconds to backoff when retrying on
                errors. Default: 100.
            exclude_internal_topics (bool): Whether records from internal topics
                (such as offsets) should be exposed to the consumer. If set to
                True the only way to receive records from an internal topic is
                subscribing to it. Requires 0.10+. Default: True
        """
        ...
    def protocol_type(self) -> str: ...
    def group_protocols(self) -> list[tuple[Incomplete, Incomplete]]:
        """Returns list of preferred (protocols, metadata)"""
        ...
    def poll(self, timeout_ms=None) -> bool:
        """
        Poll for coordinator events. Only applicable if group_id is set, and
        broker version supports GroupCoordinators. This ensures that the
        coordinator is known, and if using automatic partition assignment,
        ensures that the consumer has joined the group. This also handles
        periodic offset commits if they are enabled.
        """
        ...
    def time_to_next_poll(self):
        """Return seconds (float) remaining until :meth:`.poll` should be called again"""
        ...
    def need_rejoin(self) -> bool:
        """
        Check whether the group should be rejoined

        Returns:
            bool: True if consumer should rejoin group, False otherwise
        """
        ...
    def refresh_committed_offsets_if_needed(self, timeout_ms=None):
        """Fetch committed offsets for assigned partitions."""
        ...
    async def refresh_committed_offsets_if_needed_async(self, timeout_ms=None) -> bool: ...
    def fetch_committed_offsets(self, partitions, timeout_ms=None):
        """
        Fetch the current committed offsets for specified partitions

        Arguments:
            partitions (list of TopicPartition): partitions to fetch

        Returns:
            dict: {TopicPartition: OffsetAndMetadata}

        Raises:
            KafkaTimeoutError if timeout_ms provided
        """
        ...
    async def fetch_committed_offsets_async(self, partitions, timeout_ms=None):
        """Async variant of :meth:`fetch_committed_offsets`."""
        ...
    def close(self, autocommit: bool = True, timeout_ms=None) -> None:
        """
        Close the coordinator, leave the current group,
        and reset local generation / member_id.

        Keyword Arguments:
            autocommit (bool): If auto-commit is configured for this consumer,
                this optional flag causes the consumer to attempt to commit any
                pending consumed offsets prior to close. Default: True
        """
        ...
    def commit_offsets_async(self, offsets, callback=None):
        """
        Commit specific offsets asynchronously.

        Arguments:
            offsets (dict {TopicPartition: OffsetAndMetadata}): what to commit
            callback (callable, optional): called as callback(offsets, response)
                response will be either an Exception or a OffsetCommitResponse
                struct. This callback can be used to trigger custom actions when
                a commit request completes.

        Returns:
            kafka.future.Future
        """
        ...
    def commit_offsets_sync(self, offsets, timeout_ms=None):
        """
        Commit specific offsets synchronously.

        This method will retry until the commit completes successfully or an
        unrecoverable error is encountered.

        Arguments:
            offsets (dict {TopicPartition: OffsetAndMetadata}): what to commit

        Raises error on failure
        """
        ...
    def maybe_auto_commit_offsets_now(self) -> None: ...

class ConsumerCoordinatorMetrics:
    metrics: Incomplete
    metric_group_name: Incomplete
    commit_latency: Incomplete
    def __init__(self, metrics, metric_group_prefix, subscription) -> None: ...
