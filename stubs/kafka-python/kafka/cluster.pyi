from _typeshed import Incomplete

log: Incomplete

class ClusterMetadata:
    """
    A class to manage kafka cluster metadata.

    This class does not perform any IO. It simply updates internal state
    given API responses (MetadataResponse, FindCoordinatorResponse).

    Keyword Arguments:
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the client should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
    """
    DEFAULT_CONFIG: Incomplete
    need_all_topic_metadata: bool
    unauthorized_topics: Incomplete
    internal_topics: Incomplete
    controller: Incomplete
    cluster_id: Incomplete
    config: Incomplete
    def __init__(self, **configs) -> None: ...
    def is_bootstrap(self, node_id): ...
    def brokers(self):
        """
        Get all BrokerMetadata

        Returns:
            set: {BrokerMetadata, ...}
        """
        ...
    def broker_metadata(self, broker_id):
        """
        Get BrokerMetadata

        Arguments:
            broker_id (int or str): node_id for a broker to check

        Returns:
            BrokerMetadata or None if not found
        """
        ...
    def partitions_for_topic(self, topic):
        """
        Return set of all partitions for topic (whether available or not)

        Arguments:
            topic (str): topic to check for partitions

        Returns:
            set: {partition (int), ...}
            None if topic not found.
        """
        ...
    def available_partitions_for_topic(self, topic):
        """
        Return set of partitions with known leaders

        Arguments:
            topic (str): topic to check for partitions

        Returns:
            set: {partition (int), ...}
            None if topic not found.
        """
        ...
    def leader_for_partition(self, partition):
        """Return node_id of leader, -1 unavailable, None if unknown."""
        ...
    def leader_epoch_for_partition(self, partition): ...
    def partitions_for_broker(self, broker_id):
        """
        Return TopicPartitions for which the broker is a leader.

        Arguments:
            broker_id (int or str): node id for a broker

        Returns:
            set: {TopicPartition, ...}
            None if the broker either has no partitions or does not exist.
        """
        ...
    def coordinator_for_group(self, group):
        """
        Return node_id of group coordinator.

        Arguments:
            group (str): name of consumer group

        Returns:
            node_id (int or str) for group coordinator, -1 if coordinator unknown
            None if the group does not exist.
        """
        ...
    def ttl(self):
        """Milliseconds until metadata should be refreshed"""
        ...
    def refresh_backoff(self):
        """Return milliseconds to wait before attempting to retry after failure"""
        ...
    def request_update(self):
        """
        Flags metadata for update, return Future()

        Actual update must be handled separately. This method will only
        change the reported ttl()

        Returns:
            kafka.future.Future (value will be the cluster object after update)
        """
        ...
    @property
    def need_update(self): ...
    def topics(self, exclude_internal_topics: bool = True):
        """
        Get set of known topics.

        Arguments:
            exclude_internal_topics (bool): Whether records from internal topics
                (such as offsets) should be exposed to the consumer. If set to
                True the only way to receive records from an internal topic is
                subscribing to it. Default True

        Returns:
            set: {topic (str), ...}
        """
        ...
    def failed_update(self, exception) -> None:
        """Update cluster state given a failed MetadataRequest."""
        ...
    def update_metadata(self, metadata):
        """
        Update cluster state given a MetadataResponse.

        Arguments:
            metadata (MetadataResponse): broker response to a metadata request

        Returns: None
        """
        ...
    def add_listener(self, listener) -> None:
        """Add a callback function to be called on each metadata update"""
        ...
    def remove_listener(self, listener) -> None:
        """Remove a previously added listener callback"""
        ...
    def add_coordinator(self, response, coord_type, coord_key):
        """
        Update with metadata for a group or txn coordinator

        Arguments:
            response (FindCoordinatorResponse): broker response
            coord_type (str): 'group' or 'transaction'
            coord_key (str): consumer_group or transactional_id

        Returns:
            string: coordinator node_id if metadata is updated, None on error
        """
        ...
    def with_partitions(self, partitions_to_add):
        """Returns a copy of cluster metadata with partitions added"""
        ...

def collect_hosts(hosts, randomize: bool = True):
    """
    Collects a comma-separated set of hosts (host:port) and optionally
    randomize the returned list.
    """
    ...
