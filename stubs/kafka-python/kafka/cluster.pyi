from _typeshed import Incomplete
from socket import AddressFamily
from typing import Final

from kafka.future import Future
from kafka.protocol.metadata import CoordinatorType, MetadataRequest

class ClusterMetadata:
    """
    A class to manage kafka cluster metadata.

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
        allow_auto_create_topics (bool): Enable/disable auto topic creation
            on metadata request. Only available with api_version >= (0, 11).
            Default: True
    """
    DEFAULT_CONFIG: dict[str, Incomplete]
    need_all_topic_metadata: bool
    unauthorized_topics: Incomplete
    internal_topics: Incomplete
    controller: Incomplete
    cluster_id: Incomplete
    config: dict[str, Incomplete]
    closed: bool
    def __init__(self, **configs) -> None: ...
    @property
    def metadata_refresh_in_progress(self) -> bool:
        """True if a refresh is mid-flight."""
        ...
    def attach(self, manager) -> None:
        """
        Wire this cluster to its connection manager.

        Construction is split from attach so ClusterMetadata can be built
        standalone (tests, snapshots) without a live manager. The reference is
        held via weakref.proxy so that manager <-> cluster does not form a GC
        cycle; manager.close() still calls cluster.close() to clear eagerly.
        """
        ...
    def close(self) -> None: ...
    def start_refresh_loop(self) -> None:
        """Spawn the periodic refresh coroutine. Idempotent. Triggers bootstrap if needed."""
        ...
    async def refresh_metadata(self, node_id=None) -> None:
        """
        Send one MetadataRequest and apply the response.

        Concurrent callers share a single in-flight request: if a refresh is
        already underway, additional callers await the same Future and see the
        same outcome (success or exception). This avoids duplicate broker
        requests when bootstrap and the refresh loop race, or when external
        callers invoke refresh while the loop is mid-flight.
        """
        ...
    def is_bootstrap(self, node_id) -> bool: ...
    def set_topics(self, topics) -> Future:
        """
        Set specific topics to track for metadata.

        Arguments:
            topics (list of str): topics to check for metadata

        Returns:
            Future: resolves after metadata request/response
        """
        ...
    def add_topic(self, topic: str) -> Future:
        """
        Add a topic to the list of topics tracked via metadata.

        Arguments:
            topic (str): topic to track

        Returns:
            Future: resolves after metadata request/response

        Raises:
            TypeError: if topic is not a string
            ValueError: if topic is invalid: must be chars (a-zA-Z0-9._-), and less than 250 length
        """
        ...
    def brokers(self) -> list[Incomplete]:
        """
        Get all MetadataResponseBroker

        Returns:
            list: [MetadataResponseBroker, ...]
        """
        ...
    def bootstrap_brokers(self) -> list[Incomplete]:
        """
        Get bootstrap brokers only, extracted from the
        bootstrap_servers config option. Node ids are synthesized
        as 'bootstrap-0' etc.

        Returns:
            list: [MetadataResponseBroker, ...]
        """
        ...
    def broker_metadata(self, broker_id):
        """
        Get MetadataResponseBroker

        Arguments:
            broker_id (int or str): node_id for a broker to check

        Returns:
            MetadataResponseBroker or None if not found
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
    def is_replica_node(self, partition, node_id):
        """
        Return MetadataResponseBroker for ``node_id`` only when it is
        known AND still listed as a replica of ``partition`` (KIP-392).

        Used by the consumer's preferred-read-replica routing to avoid
        sending fetches to a broker that has been demoted out of the
        partition's replica set even though it still exists as a node.

        Arguments:
            partition (TopicPartition): topic / partition to look up.
            node_id (int): broker id to validate.

        Returns:
            MetadataResponseBroker if the node exists in cluster metadata
            and is currently listed as a replica of ``partition``;
            otherwise None.
        """
        ...
    def leader_epoch_for_partition(self, partition):
        """Return leader_epoch for partition, or None if topic/partition is unknown."""
        ...
    def update_partition_leader(self, partition, leader_id: int, leader_epoch: int) -> bool:
        """
        Apply a KIP-951 current-leader hint from a Fetch/Produce response.

        The cached leader id and epoch for ``partition`` are replaced only when
        ``leader_epoch`` is strictly newer than the cached value (and
        non-negative). When the leader id moves, ``_broker_partitions`` is
        rewired so leader-based routing follows immediately.

        Arguments:
            partition (TopicPartition): topic / partition the hint is about.
            leader_id (int): broker id named as the new leader.
            leader_epoch (int): epoch of that new leader.

        Returns:
            bool: True iff cached state was changed.
        """
        ...
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
    def get_coordinator(self, key: str, key_type: CoordinatorType = CoordinatorType.GROUP):
        """
        Return node_id of group coordinator from cache.

        Arguments:
            key (str): name of consumer group or transaction_id
            key_type (CoordinatorType, optional): Default GROUP

        Returns:
            node_id (int or str) for coordinator, -1 if coordinator unknown
            None if the group does not exist.
        """
        ...
    def ttl(self):
        """Milliseconds until metadata should be refreshed"""
        ...
    def refresh_backoff(self):
        """Return milliseconds to wait before attempting to retry after failure"""
        ...
    def request_update(self) -> Future:
        """
        Flags metadata for update, return Future()

        Actual update must be handled separately. This method will only
        change the reported ttl()

        Returns:
            kafka.future.Future (value will be the cluster object after update)
        """
        ...
    @property
    def need_update(self) -> bool: ...
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
    def metadata_request(self) -> MetadataRequest: ...
    def topic_id(self, topic_name):
        """
        Return the topic UUID for ``topic_name``, or None if unknown.

        Populated from MetadataResponse v10+ (Kafka 2.8+, KIP-516). Older
        responses leave this empty.
        """
        ...
    def topic_name_for_id(self, topic_id):
        """
        Return the topic name for ``topic_id`` (uuid.UUID), or None.

        Reverse lookup of :meth:`topic_id`. Populated from MetadataResponse
        v10+ (KIP-516).
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
        """Remove a previously added listener callback."""
        ...
    def add_coordinator(self, response, key_type: CoordinatorType, key: str, synthesize_node_id: bool = True):
        """
        Update with metadata for a group or txn coordinator

        Arguments:
            response (FindCoordinatorResponse): broker response
            key_type (CoordinatorType): GROUP / TRANSACTION / SHARE
            key (str): consumer_group or transactional_id
            synthesize_node_id (bool): If True synthesizes a unique
                node_id to generate a dedicated network connection for
                coordinator requests. Default: True.

        Returns:
            string: coordinator node_id.

        Raises:
            BrokerResponseError: if ``response.error_code`` is non-zero.
        """
        ...

def collect_hosts(hosts, randomize: bool = True) -> list[Incomplete]:
    """
    Processes a list (or comma-separated string) of hosts strings (host:port)
    and returns a list of (host, port, family) tuples.
    Optionally randomizes the returned list.
    """
    ...
def expand_to_canonical_bootstrap_hosts(hosts) -> list[Incomplete]:
    """
    Expand each bootstrap entry to one entry per canonical FQDN.

    Mirrors Java's ``client.dns.lookup=resolve_canonical_bootstrap_servers_only``:
    forward-resolve each host, take the ``canonname`` reported by the resolver,
    and emit one bootstrap entry per unique canonical name. Useful for
    Kerberos round-robin DNS deployments where the principal must match each
    individual broker FQDN.

    If a host fails to resolve, the original entry is preserved verbatim --
    matching Java's best-effort behaviour so bootstrap doesn't fail outright.
    """
    ...

DEFAULT_KAFKA_PORT: Final = 9092

def get_ip_port_afi(host_and_port_str: str) -> tuple[str, int, AddressFamily]:
    """
    Parse the IP and port from a string in the format of:

        * host_or_ip          <- Can be either IPv4 address literal or hostname/fqdn
        * host_or_ipv4:port   <- Can be either IPv4 address literal or hostname/fqdn
        * [host_or_ip]        <- IPv6 address literal
        * [host_or_ip]:port.  <- IPv6 address literal

    .. note:: IPv6 address literals with ports *must* be enclosed in brackets

    .. note:: If the port is not specified, default will be returned.

    :return: tuple (host, port, afi), afi will be socket.AF_INET or socket.AF_INET6 or socket.AF_UNSPEC
    """
    ...
