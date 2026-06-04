import selectors
import ssl
from _typeshed import Incomplete
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Literal, TypeAlias, TypedDict, type_check_only
from typing_extensions import Unpack

from kafka.admin.acl_resource import ACL, ACLFilter
from kafka.admin.config_resource import ConfigResource
from kafka.admin.new_partitions import NewPartitions
from kafka.admin.new_topic import NewTopic
from kafka.errors import KafkaError
from kafka.protocol.admin import ElectionType
from kafka.structs import GroupInformation, OffsetAndMetadata, TopicPartition

_ApiVersion: TypeAlias = tuple[int, ...]
_BootstrapServers: TypeAlias = str | Sequence[str]
_KafkaClientFactory: TypeAlias = Callable[..., object]
_SaslMechanism: TypeAlias = Literal["PLAIN", "GSSAPI", "OAUTHBEARER", "SCRAM-SHA-256", "SCRAM-SHA-512"]
_SecurityProtocol: TypeAlias = Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"]
_SocketOption: TypeAlias = tuple[int, int, int]

@type_check_only
class _KafkaAdminClientConfig(TypedDict, total=False):
    bootstrap_servers: _BootstrapServers
    client_id: str
    request_timeout_ms: int
    connections_max_idle_ms: int
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    max_in_flight_requests_per_connection: int
    receive_buffer_bytes: int | None
    send_buffer_bytes: int | None
    socket_options: Sequence[_SocketOption]
    sock_chunk_bytes: int
    sock_chunk_buffer_count: int
    retry_backoff_ms: int
    metadata_max_age_ms: int
    security_protocol: _SecurityProtocol
    ssl_context: ssl.SSLContext | None
    ssl_check_hostname: bool
    ssl_cafile: str | None
    ssl_certfile: str | None
    ssl_keyfile: str | None
    ssl_password: str | None
    ssl_crlfile: str | None
    api_version: _ApiVersion | None
    api_version_auto_timeout_ms: int
    selector: type[selectors.BaseSelector]
    sasl_mechanism: _SaslMechanism | None
    sasl_plain_username: str | None
    sasl_plain_password: str | None
    sasl_kerberos_name: object | None
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: str | None
    sasl_oauth_token_provider: object | None
    socks5_proxy: str | None
    metric_reporters: Sequence[type[object]]
    metrics_num_samples: int
    metrics_sample_window_ms: int
    kafka_client: _KafkaClientFactory

@type_check_only
class _CreateAclsResult(TypedDict):
    succeeded: list[ACL]
    failed: list[tuple[ACL, KafkaError]]

log: Incomplete

class KafkaAdminClient:
    """
    A class for administering the Kafka cluster.

    Warning:
        This is an unstable interface that was recently added and is subject to
        change without warning. In particular, many methods currently return
        raw protocol tuples. In future releases, we plan to make these into
        nicer, more pythonic objects. Unfortunately, this will likely break
        those interfaces.

    The KafkaAdminClient class will negotiate for the latest version of each message
    protocol format supported by both the kafka-python client library and the
    Kafka broker. Usage of optional fields from protocol versions that are not
    supported by the broker will result in IncompatibleBrokerVersion exceptions.

    Use of this class requires a minimum broker version >= 0.10.0.0.

    Keyword Arguments:
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the consumer should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
        client_id (str): a name for this client. This string is passed in
            each request to servers and can be used to identify specific
            server-side log entries that correspond to this client. Also
            submitted to GroupCoordinator for logging with respect to
            consumer group administration. Default: 'kafka-python-{version}'
        reconnect_backoff_ms (int): The amount of time in milliseconds to
            wait before attempting to reconnect to a given host.
            Default: 50.
        reconnect_backoff_max_ms (int): The maximum amount of time in
            milliseconds to backoff/wait when reconnecting to a broker that has
            repeatedly failed to connect. If provided, the backoff per host
            will increase exponentially for each consecutive connection
            failure, up to this maximum. Once the maximum is reached,
            reconnection attempts will continue periodically with this fixed
            rate. To avoid connection storms, a randomization factor of 0.2
            will be applied to the backoff resulting in a random range between
            20% below and 20% above the computed value. Default: 30000.
        request_timeout_ms (int): Client request timeout in milliseconds.
            Default: 30000.
        connections_max_idle_ms: Close idle connections after the number of
            milliseconds specified by this config. The broker closes idle
            connections after connections.max.idle.ms, so this avoids hitting
            unexpected socket disconnected errors on the client.
            Default: 540000
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        max_in_flight_requests_per_connection (int): Requests are pipelined
            to kafka brokers up to this number of maximum requests per
            broker connection. Default: 5.
        receive_message_max_bytes (int): Maximum allowed network frame size.
            Used to avoid OOM when decoding malformed network message header.
            Default: 1000000.
        receive_buffer_bytes (int): The size of the TCP receive buffer
            (SO_RCVBUF) to use when reading data. Default: None (relies on
            system defaults). Java client defaults to 32768.
        send_buffer_bytes (int): The size of the TCP send buffer
            (SO_SNDBUF) to use when sending data. Default: None (relies on
            system defaults). Java client defaults to 131072.
        socket_options (list): List of tuple-arguments to socket.setsockopt
            to apply to broker connection sockets. Default:
            [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        security_protocol (str): Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
        ssl_context (ssl.SSLContext): Pre-configured SSLContext for wrapping
            socket connections. If provided, all other ssl_* configurations
            will be ignored. Default: None.
        ssl_check_hostname (bool): Flag to configure whether SSL handshake
            should verify that the certificate matches the broker's hostname.
            Default: True.
        ssl_cafile (str): Optional filename of CA file to use in certificate
            verification. Default: None.
        ssl_certfile (str): Optional filename of file in PEM format containing
            the client certificate, as well as any CA certificates needed to
            establish the certificate's authenticity. Default: None.
        ssl_keyfile (str): Optional filename containing the client private key.
            Default: None.
        ssl_password (str): Optional password to be used when loading the
            certificate chain. Default: None.
        ssl_crlfile (str): Optional filename containing the CRL to check for
            certificate expiration. By default, no CRL check is done. When
            providing a file, only the leaf certificate will be checked against
            this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+.
            Default: None.
        api_version (tuple): Specify which Kafka API version to use. If set
            to None, KafkaClient will attempt to infer the broker version by
            probing various APIs. Example: (0, 10, 2). Default: None
        api_version_auto_timeout_ms (int): number of milliseconds to throw a
            timeout exception from the constructor when checking the broker
            api version. Only applies if api_version is None
        selector (selectors.BaseSelector): Provide a specific selector
            implementation to use for I/O multiplexing.
            Default: selectors.DefaultSelector
        metrics (kafka.metrics.Metrics): Optionally provide a metrics
            instance for capturing network IO stats. Default: None.
        metric_group_prefix (str): Prefix for metric names. Default: ''
        sasl_mechanism (str): Authentication mechanism when security_protocol
            is configured for SASL_PLAINTEXT or SASL_SSL. Valid values are:
            PLAIN, GSSAPI, OAUTHBEARER, SCRAM-SHA-256, SCRAM-SHA-512.
        sasl_plain_username (str): username for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_plain_password (str): password for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_kerberos_name (str or gssapi.Name): Constructed gssapi.Name for use with
            sasl mechanism handshake. If provided, sasl_kerberos_service_name and
            sasl_kerberos_domain name are ignored. Default: None.
        sasl_kerberos_service_name (str): Service name to include in GSSAPI
            sasl mechanism handshake. Default: 'kafka'
        sasl_kerberos_domain_name (str): kerberos domain name to use in GSSAPI
            sasl mechanism handshake. Default: one of bootstrap servers
        sasl_oauth_token_provider (kafka.sasl.oauth.AbstractTokenProvider): OAuthBearer
            token provider instance. Default: None
        socks5_proxy (str): Socks5 proxy url. Default: None
        kafka_client (callable): Custom class / callable for creating KafkaClient instances
    """
    DEFAULT_CONFIG: Incomplete
    config: Incomplete
    def __init__(self, **configs: Unpack[_KafkaAdminClientConfig]) -> None: ...
    def close(self) -> None:
        """Close the KafkaAdminClient connection to the Kafka broker."""
        ...
    def send_request(self, request, node_id=None): ...
    def send_requests(self, requests_and_node_ids, response_fn=...): ...
    def create_topics(self, new_topics: Sequence[NewTopic], timeout_ms: int | None = None, validate_only: bool = False):
        """
        Create new topics in the cluster.

        Arguments:
            new_topics: A list of NewTopic objects.

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for new topics to be created
                before the broker returns.
            validate_only (bool, optional): If True, don't actually create new topics.
                Not supported by all versions. Default: False

        Returns:
            Appropriate version of CreateTopicResponse class.
        """
        ...
    def delete_topics(self, topics: Sequence[str], timeout_ms: int | None = None):
        """
        Delete topics from the cluster.

        Arguments:
            topics ([str]): A list of topic name strings.

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for topics to be deleted
                before the broker returns.

        Returns:
            Appropriate version of DeleteTopicsResponse class.
        """
        ...
    def list_topics(self) -> list[str]:
        """
        Retrieve a list of all topic names in the cluster.

        Returns:
            A list of topic name strings.
        """
        ...
    def describe_topics(self, topics: Sequence[str] | None = None) -> list[dict[str, Incomplete]]:
        """
        Fetch metadata for the specified topics or all topics if None.

        Keyword Arguments:
            topics ([str], optional) A list of topic names. If None, metadata for all
                topics is retrieved.

        Returns:
            A list of dicts describing each topic (including partition info).
        """
        ...
    def describe_cluster(self) -> dict[str, Incomplete]:
        """
        Fetch cluster-wide metadata such as the list of brokers, the controller ID,
        and the cluster ID.


        Returns:
            A dict with cluster-wide metadata, excluding topic details.
        """
        ...
    def describe_acls(self, acl_filter: ACLFilter) -> tuple[list[ACL], KafkaError]:
        """
        Describe a set of ACLs

        Used to return a set of ACLs matching the supplied ACLFilter.
        The cluster must be configured with an authorizer for this to work, or
        you will get a SecurityDisabledError

        Arguments:
            acl_filter: an ACLFilter object

        Returns:
            tuple of a list of matching ACL objects and a KafkaError (NoError if successful)
        """
        ...
    def create_acls(self, acls: Sequence[ACL]) -> _CreateAclsResult:
        """
        Create a list of ACLs

        This endpoint only accepts a list of concrete ACL objects, no ACLFilters.
        Throws TopicAlreadyExistsError if topic is already present.

        Arguments:
            acls: a list of ACL objects

        Returns:
            dict of successes and failures
        """
        ...
    def delete_acls(
        self, acl_filters: Sequence[ACLFilter]
    ) -> list[tuple[ACLFilter, list[tuple[ACL, KafkaError]], KafkaError]]:
        """
        Delete a set of ACLs

        Deletes all ACLs matching the list of input ACLFilter

        Arguments:
            acl_filters: a list of ACLFilter

        Returns:
            a list of 3-tuples corresponding to the list of input filters.
                 The tuples hold (the input ACLFilter, list of affected ACLs, KafkaError instance)
        """
        ...
    def describe_configs(self, config_resources: Sequence[ConfigResource], include_synonyms: bool = False):
        """
        Fetch configuration parameters for one or more Kafka resources.

        Arguments:
            config_resources: An list of ConfigResource objects.
                Any keys in ConfigResource.configs dict will be used to filter the
                result. Setting the configs dict to None will get all values. An
                empty dict will get zero values (as per Kafka protocol).

        Keyword Arguments:
            include_synonyms (bool, optional): If True, return synonyms in response. Not
                supported by all versions. Default: False.

        Returns:
            List of DescribeConfigsResponses.
        """
        ...
    def alter_configs(self, config_resources: Sequence[ConfigResource]):
        """
        Alter configuration parameters of one or more Kafka resources.

        Warning:
            This is currently broken for BROKER resources because those must be
            sent to that specific broker, versus this always picks the
            least-loaded node. See the comment in the source code for details.
            We would happily accept a PR fixing this.

        Arguments:
            config_resources: A list of ConfigResource objects.

        Returns:
            Appropriate version of AlterConfigsResponse class.
        """
        ...
    def create_partitions(
        self, topic_partitions: Mapping[str, NewPartitions], timeout_ms: int | None = None, validate_only: bool = False
    ):
        """
        Create additional partitions for an existing topic.

        Arguments:
            topic_partitions: A map of topic name strings to NewPartition objects.

        Keyword Arguments:
            timeout_ms (numeric, optional): Milliseconds to wait for new partitions to be
                created before the broker returns.
            validate_only (bool, optional): If True, don't actually create new partitions.
                Default: False

        Returns:
            Appropriate version of CreatePartitionsResponse class.
        """
        ...
    def delete_records(
        self,
        records_to_delete: Mapping[TopicPartition, int],
        timeout_ms: float | None = None,
        partition_leader_id: int | None = None,
    ) -> dict[TopicPartition, Incomplete]:
        """
        Delete records whose offset is smaller than the given offset of the corresponding partition.

        :param records_to_delete: ``{TopicPartition: int}``: The earliest available offsets for the
            given partitions.
        :param timeout_ms: ``float``: Timeout in milliseconds, if None (default), will be read from
            config.
        :param partition_leader_id: ``str``: If specified, all deletion requests will be sent to
            this node. No check is performed verifying that this is indeed the leader for all
            listed partitions: use with caution.

        :return: Dictionary {topicPartition -> metadata}, where metadata is returned by the broker.
            See DeleteRecordsResponse for possible fields. error_code for all partitions is
            guaranteed to be zero, otherwise an exception is raised.
        """
        ...
    def describe_consumer_groups(
        self, group_ids: Sequence[str], group_coordinator_id: int | None = None, include_authorized_operations: bool = False
    ) -> list[GroupInformation]:
        """
        Describe a set of consumer groups.

        Any errors are immediately raised.

        Arguments:
            group_ids: A list of consumer group IDs. These are typically the
                group names as strings.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the groups' coordinator
                broker. If set to None, it will query the cluster for each group to
                find that group's coordinator. Explicitly specifying this can be
                useful for avoiding extra network round trips if you already know
                the group coordinator. This is only useful when all the group_ids
                have the same coordinator, otherwise it will error. Default: None.

        Returns:
            A list of group descriptions. For now the group descriptions
            are the raw results from the DescribeGroupsResponse. Long-term, we
            plan to change this to return namedtuples as well as decoding the
            partition assignments.
        """
        ...
    def list_consumer_groups(self, broker_ids: Sequence[int] | None = None) -> list[tuple[str, str]]:
        """
        List all consumer groups known to the cluster.

        This returns a list of Consumer Group tuples. The tuples are
        composed of the consumer group name and the consumer group protocol
        type.

        Only consumer groups that store their offsets in Kafka are returned.
        The protocol type will be an empty string for groups created using
        Kafka < 0.9 APIs because, although they store their offsets in Kafka,
        they don't use Kafka for group coordination. For groups created using
        Kafka >= 0.9, the protocol type will typically be "consumer".

        As soon as any error is encountered, it is immediately raised.

        Keyword Arguments:
            broker_ids ([int], optional): A list of broker node_ids to query for consumer
                groups. If set to None, will query all brokers in the cluster.
                Explicitly specifying broker(s) can be useful for determining which
                consumer groups are coordinated by those broker(s). Default: None

        Returns:
            list: List of tuples of Consumer Groups.

        Raises:
            CoordinatorNotAvailableError: The coordinator is not
                available, so cannot process requests.
            CoordinatorLoadInProgressError: The coordinator is loading and
                hence can't process requests.
        """
        ...
    def list_consumer_group_offsets(
        self, group_id: str, group_coordinator_id: int | None = None, partitions: Iterable[TopicPartition] | None = None
    ) -> dict[TopicPartition, OffsetAndMetadata]:
        """
        Fetch Consumer Offsets for a single consumer group.

        Note:
        This does not verify that the group_id or partitions actually exist
        in the cluster.

        As soon as any error is encountered, it is immediately raised.

        Arguments:
            group_id (str): The consumer group id name for which to fetch offsets.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the group's coordinator
                broker. If set to None, will query the cluster to find the group
                coordinator. Explicitly specifying this can be useful to prevent
                that extra network round trip if you already know the group
                coordinator. Default: None.
            partitions: A list of TopicPartitions for which to fetch
                offsets. On brokers >= 0.10.2, this can be set to None to fetch all
                known offsets for the consumer group. Default: None.

        Returns:
            dictionary: A dictionary with TopicPartition keys and
            OffsetAndMetadata values. Partitions that are not specified and for
            which the group_id does not have a recorded offset are omitted. An
            offset value of `-1` indicates the group_id has no offset for that
            TopicPartition. A `-1` can only happen for partitions that are
            explicitly specified.
        """
        ...
    def delete_consumer_groups(
        self, group_ids: Sequence[str], group_coordinator_id: int | None = None
    ) -> list[tuple[str, KafkaError]]:
        """
        Delete Consumer Group Offsets for given consumer groups.

        Note:
        This does not verify that the group ids actually exist and
        group_coordinator_id is the correct coordinator for all these groups.

        The result needs checking for potential errors.

        Arguments:
            group_ids ([str]): The consumer group ids of the groups which are to be deleted.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the broker which is
                the coordinator for all the groups. Use only if all groups are coordinated
                by the same broker. If set to None, will query the cluster to find the coordinator
                for every single group. Explicitly specifying this can be useful to prevent
                that extra network round trips if you already know the group coordinator.
                Default: None.

        Returns:
            A list of tuples (group_id, KafkaError)
        """
        ...
    def perform_leader_election(
        self,
        election_type: int | ElectionType,
        topic_partitions: Mapping[str, Sequence[int]] | None = None,
        timeout_ms: int | None = None,
    ):
        """
        Perform leader election on the topic partitions.

        :param election_type: Type of election to attempt. 0 for Perferred, 1 for Unclean
        :param topic_partitions: A map of topic name strings to partition ids list.
            By default, will run on all topic partitions
        :param timeout_ms: Milliseconds to wait for the leader election process to complete
            before the broker returns.

        :return: Appropriate version of ElectLeadersResponse class.
        """
        ...
    def describe_log_dirs(self):
        """
        Send a DescribeLogDirsRequest request to a broker.

        Returns:
            DescribeLogDirsResponse object
        """
        ...
