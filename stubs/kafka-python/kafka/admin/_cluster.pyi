"""Cluster metadata mixin for KafkaAdminClient."""

from _typeshed import Incomplete
from enum import IntEnum

from kafka.protocol.api_key import ApiKey
from kafka.util import EnumHelper

class ClusterAdminMixin:
    """Mixin providing cluster management methods for KafkaAdminClient."""
    def describe_cluster(self) -> dict[str, Incomplete]:
        """
        Fetch cluster-wide metadata such as the list of brokers, the controller ID,
        and the cluster ID.

        Returns:
            A dict with cluster-wide metadata, excluding topic details.
        """
        ...
    def describe_log_dirs(
        self,
        topic_partitions: dict[Incomplete, Incomplete] | list[Incomplete] | None = None,
        brokers: list[Incomplete] | None = None,
    ) -> list[dict[str, Incomplete]]:
        """
        Fetch broker log directory and topic/partition stats

        Keyword Arguments:
            topic_partitions (dict, list, optional):
                Either: dict of {topic_name: [partition ids]}.
                Or:     list of [topic_name], to query all partitions for topic.
                Or:     None, to query all topics / all partitions.
                Default: None
            brokers (list, optional): List of [node_id] for brokers to query.
                If None, query is sent to all brokers. Default: None

        Returns:
            list of dicts, containing per-broker log-dir data
        """
        ...
    def alter_replica_log_dirs(self, replica_assignments):
        """
        Move replicas between log directories on their hosting brokers.

        Each entry instructs the targeted broker to move (or place) the
        replica for a given partition into the specified absolute log
        directory path. Requests are sent to each broker in parallel; a
        broker will only act on replicas it currently hosts.

        Arguments:
            replica_assignments: A dict mapping
                :class:`~kafka.TopicPartitionReplica` (``topic``,
                ``partition``, ``broker_id``) to the destination log
                directory path (absolute string). Tuples of
                ``(topic, partition, broker_id)`` are also accepted.

        Returns:
            dict mapping :class:`~kafka.TopicPartitionReplica` to the
            corresponding error class (``kafka.errors.NoError`` on success).
        """
        ...
    def describe_metadata_quorum(self):
        """
        Describe the KRaft quorum state for the cluster metadata log.

        Returns quorum info for the ``__cluster_metadata`` topic
        (partition 0), including the current leader, leader epoch, high
        watermark, voters, and observers. On broker version >= 3.8 (KIP-853),
        the response also reports controller node endpoints in ``nodes``.
        Requires a KRaft cluster.

        Returns:
            dict matching the DescribeQuorumResponse shape.
        """
        ...
    def get_broker_version_data(self, broker_id):
        """Return BrokerVersionData for a specific broker"""
        ...
    def api_versions(self) -> dict[ApiKey, tuple[int, int] | Incomplete]: ...
    def describe_features(self, send_request_to_controller: bool = False) -> dict[str, Incomplete]:
        """
        Fetch the cluster's supported and finalized feature flags.

        Features are broker-level capabilities (e.g. ``metadata.version``)
        that can be finalized cluster-wide via ``update_features`` (KIP-584).
        Requires broker >= 2.4.

        Keyword Arguments:
            send_request_to_controller (bool, optional): If True, route the
                request to the active controller. By default the request is
                sent to any available broker. Default: False.

        Returns:
            dict with keys:
                - ``supported_features``: dict of
                  ``{feature_name: (min_version, max_version)}``
                - ``finalized_features``: dict of
                  ``{feature_name: (min_version_level, max_version_level)}``
                - ``finalized_features_epoch``: int, or None if unknown
                  (broker did not report an epoch, or reported -1)
        """
        ...
    def update_features(
        self, feature_updates: dict[Incomplete, Incomplete], validate_only: bool = False, timeout_ms: int = 60000
    ) -> dict[Incomplete, Incomplete]:
        """
        Update cluster-wide finalized feature flags.

        Finalize cluster-wide feature capabilities (e.g. ``metadata.version``).
        The request is always routed to the active controller. See KIP-584.
        Requires broker >= 2.7.

        Arguments:
            feature_updates: A dict of
                ``{feature_name: (upgrade_type, max_version_level)}`` or
                ``{feature_name: max_version_level}`` (implicit UPGRADE).
                ``upgrade_type`` may be a :class:`UpdateFeatureType`,
                its name, or int value. A ``max_version_level < 1`` requests
                deletion of the finalized feature.

        Keyword Arguments:
            validate_only (bool, optional): If True, validate the request but
                do not apply it. Default: False.
            timeout_ms (int, optional): Broker-side timeout in milliseconds.
                Default: 60000.

        Returns:
            dict of {feature_name: 'OK' | error message}
        """
        ...

class UpdateFeatureType(EnumHelper, IntEnum):
    """An enumeration."""
    UNKNOWN = 0
    UPGRADE = 1
    SAFE_DOWNGRADE = 2
    UNSAFE_DOWNGRADE = 3
