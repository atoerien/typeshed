"""
Partition management mixin for KafkaAdminClient.

Also defines NewPartitions data class.
"""

from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from typing_extensions import deprecated

from kafka.protocol.consumer import IsolationLevel, OffsetSpec as OffsetSpec, OffsetTimestamp as OffsetTimestamp
from kafka.structs import TopicPartition

class PartitionAdminMixin:
    """Mixin providing partition and record management methods."""
    config: dict[Incomplete, Incomplete]
    def create_partitions(
        self,
        topic_partitions: Mapping[str, int | dict[Incomplete, Incomplete] | NewPartitions],
        timeout_ms: int | None = None,
        validate_only: bool = False,
        raise_errors: bool = True,
    ):
        """
        Create additional partitions for an existing topic.

        Arguments:
            topic_partitions: A dict of topic name strings to total partition count (int),
                or a dict of {topic_name: {count: int, assignments: [[broker_ids]]}}
                if manual assignment is desired.
                dict of {topic_name: NewPartitions} is deprecated.

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for new partitions to be
                created before the broker returns.
            validate_only (bool, optional): If True, don't actually create new partitions.
                Default: False
            raise_errors (bool, optional): Whether to raise errors as exceptions. Default True.

        Returns:
            Appropriate version of CreatePartitionsResponse class.
        """
        ...
    def delete_records(
        self, records_to_delete: Mapping[TopicPartition, int], timeout_ms: float | None = None, partition_leader_id=None
    ) -> dict[TopicPartition, Incomplete]:
        """
        Delete records whose offset is smaller than the given offset of the corresponding partition.

        Partitions whose response is :class:`~kafka.errors.NotLeaderForPartitionError`
        are retried with refreshed metadata, bounded by ``timeout_ms`` (or the
        admin client's ``request_timeout_ms`` when ``None``). When
        ``partition_leader_id`` is supplied no retry is attempted; the caller
        is asserting routing and any error is reported as-is.

        Arguments:
            records_to_delete ({TopicPartition: int}): The earliest available offsets for the
                given partitions.

        Keyword Arguments:
            timeout_ms (numeric, optional): Timeout in milliseconds. Also caps
                the total time spent retrying NotLeaderForPartitionError.
            partition_leader_id (node_id / int, optional): If specified, all deletion requests
                will be sent to this node.

        Returns:
            dict {topicPartition -> metadata}
        """
        ...
    def elect_leaders(self, election_type, topic_partitions=None, timeout_ms=None, raise_errors: bool = True):
        """
        Trigger leader election for the specified topic partitions.

        Arguments:
            election_type: Type of election to attempt. 0 for Preferred, 1 for Unclean

        Keyword Arguments:
            topic_partitions (dict, list, optional):
                Either: dict of {topic_name: [partition ids]}.
                Or:     list of [topic_name], and election will run on all partitions for topic.
                Or:     None, and election runs against all topics / all partitions.
                Default: None
            timeout_ms (num, optional): Milliseconds to wait for the leader election process.
            raise_errors (bool, optional): Whether to raise errors as exceptions. Default True.

        Returns:
            Appropriate version of ElectLeadersResponse class.
        """
        ...
    def alter_partition_reassignments(self, reassignments, timeout_ms=None):
        """
        Alter the replica sets for the given partitions.

        Arguments:
            reassignments (dict): A dict mapping
                :class:`~kafka.TopicPartition` to a list of broker IDs
                for the new replica set, or ``None`` to cancel a
                pending reassignment for that partition.

        Keyword Arguments:
            timeout_ms (numeric, optional): The time in ms to wait for
                the request to complete.

        Raises: top-level failures that prevents processing request.
            Does not raise partition-specific errors.

        Returns:
            dict: A dict mapping each :class:`~kafka.TopicPartition`
            that the broker acknowledged to the error class for that
            partition, or ``None`` if the reassignment was accepted.
            Partitions the broker did not report on are absent from the
            dict.
        """
        ...
    def list_partition_reassignments(self, topic_partitions=None, timeout_ms=None):
        """
        List the current ongoing partition reassignments.

        Arguments:
            topic_partitions (dict, list, optional):
                Either: a dict of ``{topic_name: [partition_ids]}``,
                or a list of :class:`~kafka.TopicPartition`,
                or ``None`` to list ongoing reassignments for all partitions.
                Default: None.

        Keyword Arguments:
            timeout_ms (numeric, optional): The time in ms to wait for the
                request to complete.

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to a dict
            with keys ``'replicas'``, ``'adding_replicas'``, and
            ``'removing_replicas'`` (each a list of broker IDs).
        """
        ...
    def describe_topic_partitions(self, topics, response_partition_limit: int = 2000, cursor=None):
        """
        Describe topics with fine-grained partition-level control (KIP-966).

        Unlike :meth:`describe_topics`, this uses the DescribeTopicPartitions
        API (apiKey 75, broker 3.7+) which supports pagination via a cursor
        and partition-level ELR (Eligible Leader Replicas) information.

        Arguments:
            topics ([str]): A list of topic names.

        Keyword Arguments:
            response_partition_limit (int, optional): Maximum number of
                partitions to include in the response. Default: 2000.
            cursor (dict, optional): Dict with ``'topic_name'`` and
                ``'partition_index'`` keys to start pagination from. Default:
                None.

        Returns:
            dict: ``{'topics': [...], 'next_cursor': None | {...}}``.
            ``topics`` is a list of dicts (one per topic) with keys
            ``error_code``, ``name``, ``topic_id``, ``is_internal``,
            ``partitions``, and ``topic_authorized_operations``.
            ``next_cursor`` is None if pagination is complete, otherwise a
            dict with the next page's ``topic_name`` and ``partition_index``.
        """
        ...
    def list_partition_offsets(
        self, topic_partition_specs, isolation_level: IsolationLevel = IsolationLevel.READ_UNCOMMITTED, timeout_ms=None
    ):
        """
        Look up offsets for the given partitions by spec.

        Partitions are routed to their respective leader brokers via cluster
        metadata; one ``ListOffsetsRequest`` is sent per leader. Partitions
        that return :class:`~kafka.errors.NotLeaderForPartitionError` are
        retried with refreshed metadata, bounded by ``timeout_ms`` (or the
        admin client's ``request_timeout_ms`` when ``None``).

        Arguments:
            topic_partition_specs: dict mapping :class:`~kafka.TopicPartition` to
                :class:`OffsetSpec` (or a raw integer timestamp /
                wire-level sentinel).

        Keyword Arguments:
            isolation_level (IsolationLevel, optional): Requires broker support
                for ListOffsets v2+. Default: IsolationLevel.READ_UNCOMMITTED.
            timeout_ms (int, optional): Maximum time to spend retrying
                NotLeaderForPartitionError. Default: ``request_timeout_ms``.

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to
            :class:`~kafka.structs.OffsetAndTimestamp`

        Raises:
            KafkaError: If any partition response carries an error code.
            NotLeaderForPartitionError: If NotLeaderForPartitionError retries
                do not converge within ``timeout_ms``.
            UnknownTopicOrPartitionError: If a requested partition is not
                known to the cluster.
            UnsupportedVersionError: If the broker does not support a version
                of ListOffsetsRequest compatible with the requested specs.
        """
        ...

@deprecated("Deprecated since v3.0.0. Use simple `dict` instead.")
class NewPartitions:
    """
    DEPRECATED: A class for new partition creation on existing topics.

    Note that the length of new_assignments, if specified, must be the
    difference between the new total number of partitions and the existing
    number of partitions.

    Arguments:
        total_count (int): the total number of partitions that should exist
            on the topic
        new_assignments ([[int]]): an array of arrays of replica assignments
            for new partitions. If not set, broker assigns replicas per an
            internal algorithm.
    """
    total_count: int
    new_assignments: Sequence[Sequence[int]] | None
    def __init__(self, total_count: int, new_assignments: Sequence[Sequence[int]] | None = None) -> None: ...
