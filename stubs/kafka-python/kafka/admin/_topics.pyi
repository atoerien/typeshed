"""
Topic management mixin for KafkaAdminClient.

Also defines NewTopic data class.
"""

import uuid
from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from typing_extensions import deprecated

class TopicAdminMixin:
    """Mixin providing topic management methods for KafkaAdminClient."""
    config: dict[Incomplete, Incomplete]
    def list_topics(self) -> list[str]:
        """
        Retrieve a list of all topic names in the cluster.

        Returns:
            A list of topic name strings.
        """
        ...
    def describe_topics(self, topics: Sequence[str | uuid.UUID] | None = None) -> list[dict[str, Incomplete]]:
        """
        Fetch metadata for the specified topics or all topics if None.

        Keyword Arguments:
            topics (list, optional): A list of topic names or
                :class:`uuid.UUID` topic ids (KIP-516). Strings and UUIDs may
                be mixed. Describing by id requires broker >= 2.8
                (MetadataRequest v12+); name-based describe works on any
                broker. If None, metadata for all topics is retrieved.

        Returns:
            A list of dicts describing each topic (including partition info).
        """
        ...
    def create_topics(
        self,
        new_topics: dict[str, dict[Incomplete, Incomplete]] | Sequence[NewTopic],
        timeout_ms: float | None = None,
        validate_only: bool = False,
        raise_errors: bool = True,
        wait_for_metadata: bool = False,
    ):
        """
        Create new topics in the cluster.

        Arguments:
            new_topics: A list of topic names, or a dict mapping each topic
                name to a dict of options (all keys optional)::

                    {topic_name: {num_partitions: int (default -1),
                                  replication_factor: int (default -1),
                                  assignments: {partition_id: [broker_ids]},
                                  configs: {key: value}}}

                List of NewTopic objects is deprecated.
                Note: for brokers < 2.4, num_partitions and replication_factor
                are required and must be provided via dict or [NewTopic].

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for new topics to be created
                before the broker returns.
            validate_only (bool, optional): If True, don't actually create new topics.
                Not supported by all versions. Default: False
            raise_errors (bool, optional): Whether to raise errors as exceptions. Default True.
            wait_for_metadata (bool, optional): If True, block until each new topic is visible
                in broker metadata with a leader assigned for every partition. Default: False

        Returns:
            dict of CreateTopicsResponse key/vals.
        """
        ...
    def wait_for_topics(self, topic_names, timeout_ms: float | None = 10000):
        """
        Block until each of the given topics is ready to use.

        CreateTopicsResponse only confirms that the broker accepted the create
        request; propagating the new topics into the broker's metadata cache --
        and electing a leader for every partition -- can lag behind, especially
        on KRaft clusters. This method polls :meth:`describe_topics` at a fixed
        interval until every requested topic both:

          - is returned with ``error_code == 0``, and
          - has ``error_code == 0`` and a leader assigned (``leader_id >= 0``)
            for every partition.

        Arguments:
            topic_names ([str]): Topic names to wait for.

        Keyword Arguments:
            timeout_ms (numeric, optional): Maximum milliseconds to wait.
                Default: 10000.

        Raises:
            KafkaTimeoutError: if any topic is still not ready when the
                deadline expires.
        """
        ...
    def delete_topics(self, topics: Sequence[str | uuid.UUID], timeout_ms: float | None = None, raise_errors: bool = True):
        """
        Delete topics from the cluster.

        Arguments:
            topics ([str]): A list of topic name strings or uuid.UUID ids.

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for topics to be deleted
                before the broker returns.
            raise_errors (bool, optional): Whether to raise errors as exceptions. Default True.

        Returns:
            dict of DeleteTopicsResponse key/vals (version-dependent)
        """
        ...

@deprecated("Deprecated since v3.0.0. Use simple `dict` instead.")
class NewTopic:
    """
    DEPRECATED: A class for new topic creation.

    Arguments:
        name (string): name of the topic
        num_partitions (int): number of partitions, or -1 if
            replica_assignment has been specified
        replication_factor (int): replication factor, or -1 if
            replica assignment is specified
        replica_assignments (dict of int: [int]): A mapping containing
            partition id and replicas to assign to it.
        topic_configs (dict of str: str): A mapping of config key
            and value for the topic.
    """
    name: str
    num_partitions: int
    replication_factor: int
    replica_assignments: Mapping[int, Sequence[int]] | None
    topic_configs: Mapping[str, str] | None
    def __init__(
        self,
        name: str,
        num_partitions: int = -1,
        replication_factor: int = -1,
        replica_assignments: Mapping[int, Sequence[int]] | None = None,
        topic_configs: Mapping[str, str] | None = None,
    ) -> None: ...
