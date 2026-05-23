import selectors
import ssl
from _typeshed import Incomplete
from collections.abc import Callable, Mapping, Sequence
from typing import Literal, TypeAlias, TypedDict, type_check_only
from typing_extensions import Unpack

from kafka.producer.future import FutureRecordMetadata
from kafka.serializer.abstract import Serializer
from kafka.structs import OffsetAndMetadata, TopicPartition

_ApiVersion: TypeAlias = tuple[int, ...]
_BootstrapServers: TypeAlias = str | Sequence[str]
_KafkaClientFactory: TypeAlias = Callable[..., object]
_Partitioner: TypeAlias = Callable[[bytes | None, Sequence[int], Sequence[int]], int]
_ProducerSerializer: TypeAlias = Serializer | Callable[[object], bytes]
_SaslMechanism: TypeAlias = Literal["PLAIN", "GSSAPI", "OAUTHBEARER", "SCRAM-SHA-256", "SCRAM-SHA-512"]
_SecurityProtocol: TypeAlias = Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"]
_SocketOption: TypeAlias = tuple[int, int, int]

@type_check_only
class _KafkaProducerConfig(TypedDict, total=False):
    bootstrap_servers: _BootstrapServers
    client_id: str | None
    key_serializer: _ProducerSerializer | None
    value_serializer: _ProducerSerializer | None
    enable_idempotence: bool
    transactional_id: str | None
    transaction_timeout_ms: int
    delivery_timeout_ms: float
    acks: int | Literal["all"]
    bootstrap_topics_filter: set[str]
    compression_type: Literal["gzip", "snappy", "lz4", "zstd"] | None
    retries: int | float
    batch_size: int
    linger_ms: int
    partitioner: _Partitioner
    connections_max_idle_ms: int
    max_block_ms: int
    max_request_size: int
    allow_auto_create_topics: bool
    metadata_max_age_ms: int
    retry_backoff_ms: int
    request_timeout_ms: int
    receive_buffer_bytes: int | None
    send_buffer_bytes: int | None
    socket_options: Sequence[_SocketOption]
    sock_chunk_bytes: int
    sock_chunk_buffer_count: int
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    max_in_flight_requests_per_connection: int
    security_protocol: _SecurityProtocol
    ssl_context: ssl.SSLContext | None
    ssl_check_hostname: bool
    ssl_cafile: str | None
    ssl_certfile: str | None
    ssl_keyfile: str | None
    ssl_crlfile: str | None
    ssl_password: str | None
    ssl_ciphers: str | None
    api_version: _ApiVersion | None
    api_version_auto_timeout_ms: int
    metric_reporters: Sequence[type[object]]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    selector: type[selectors.BaseSelector]
    sasl_mechanism: _SaslMechanism | None
    sasl_plain_username: str | None
    sasl_plain_password: str | None
    sasl_kerberos_name: object | None
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: str | None
    sasl_oauth_token_provider: object | None
    socks5_proxy: str | None
    kafka_client: _KafkaClientFactory

log: Incomplete
PRODUCER_CLIENT_ID_SEQUENCE: Incomplete

class KafkaProducer:
    """
    A Kafka client that publishes records to the Kafka cluster.

    The producer is thread safe and sharing a single producer instance across
    threads will generally be faster than having multiple instances.

    The producer consists of a RecordAccumulator which holds records that
    haven't yet been transmitted to the server, and a Sender background I/O
    thread that is responsible for turning these records into requests and
    transmitting them to the cluster.

    :meth:`~kafka.KafkaProducer.send` is asynchronous. When called it adds the
    record to a buffer of pending record sends and immediately returns. This
    allows the producer to batch together individual records for efficiency.

    The 'acks' config controls the criteria under which requests are considered
    complete. The "all" setting will result in blocking on the full commit of
    the record, the slowest but most durable setting.

    If the request fails, the producer can automatically retry, unless
    'retries' is configured to 0. Enabling retries also opens up the
    possibility of duplicates (see the documentation on message
    delivery semantics for details:
    https://kafka.apache.org/documentation.html#semantics
    ).

    The producer maintains buffers of unsent records for each partition. These
    buffers are of a size specified by the 'batch_size' config. Making this
    larger can result in more batching, but requires more memory (since we will
    generally have one of these buffers for each active partition).

    By default a buffer is available to send immediately even if there is
    additional unused space in the buffer. However if you want to reduce the
    number of requests you can set 'linger_ms' to something greater than 0.
    This will instruct the producer to wait up to that number of milliseconds
    before sending a request in hope that more records will arrive to fill up
    the same batch. This is analogous to Nagle's algorithm in TCP. Note that
    records that arrive close together in time will generally batch together
    even with linger_ms=0 so under heavy load batching will occur regardless of
    the linger configuration; however setting this to something larger than 0
    can lead to fewer, more efficient requests when not under maximal load at
    the cost of a small amount of latency.

    The key_serializer and value_serializer instruct how to turn the key and
    value objects the user provides into bytes.

    From Kafka 0.11, the KafkaProducer supports two additional modes:
    the idempotent producer and the transactional producer.
    The idempotent producer strengthens Kafka's delivery semantics from
    at least once to exactly once delivery. In particular, producer retries
    will no longer introduce duplicates. The transactional producer allows an
    application to send messages to multiple partitions (and topics!)
    atomically.

    To enable idempotence, the `enable_idempotence` configuration must be set
    to True. If set, the `retries` config will default to `float('inf')` and
    the `acks` config will default to 'all'. There are no API changes for the
    idempotent producer, so existing applications will not need to be modified
    to take advantage of this feature.

    To take advantage of the idempotent producer, it is imperative to avoid
    application level re-sends since these cannot be de-duplicated. As such, if
    an application enables idempotence, it is recommended to leave the
    `retries` config unset, as it will be defaulted to `float('inf')`.
    Additionally, if a :meth:`~kafka.KafkaProducer.send` returns an error even
    with infinite retries (for instance if the message expires in the buffer
    before being sent), then it is recommended to shut down the producer and
    check the contents of the last produced message to ensure that it is not
    duplicated. Finally, the producer can only guarantee idempotence for
    messages sent within a single session.

    To use the transactional producer and the attendant APIs, you must set the
    `transactional_id` configuration property. If the `transactional_id` is
    set, idempotence is automatically enabled along with the producer configs
    which idempotence depends on. Further, topics which are included in
    transactions should be configured for durability. In particular, the
    `replication.factor` should be at least `3`, and the `min.insync.replicas`
    for these topics should be set to 2. Finally, in order for transactional
    guarantees to be realized from end-to-end, the consumers must be
    configured to read only committed messages as well.

    The purpose of the `transactional_id` is to enable transaction recovery
    across multiple sessions of a single producer instance. It would typically
    be derived from the shard identifier in a partitioned, stateful,
    application. As such, it should be unique to each producer instance running
    within a partitioned application.

    Keyword Arguments:
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the producer should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
        client_id (str): a name for this client. This string is passed in
            each request to servers and can be used to identify specific
            server-side log entries that correspond to this client.
            Default: 'kafka-python-producer-#' (appended with a unique number
            per instance)
        key_serializer (callable): used to convert user-supplied keys to bytes
            If not None, called as f(key), should return bytes. Default: None.
        value_serializer (callable): used to convert user-supplied message
            values to bytes. If not None, called as f(value), should return
            bytes. Default: None.
        transactional_id (str): Enable transactional producer with a unique
            identifier. This will be used to identify the same producer
            instance across process restarts. Default: None.
        enable_idempotence (bool): When set to True, the producer will ensure
            that exactly one copy of each message is written in the stream.
            If False, producer retries due to broker failures, etc., may write
            duplicates of the retried message in the stream.
            Default: True if `transactional_id` is provided, otherwise False.

            Note that enabling idempotence requires
            `max_in_flight_requests_per_connection` to be set to 1 and `retries`
            cannot be zero. Additionally, `acks` must be set to 'all'. If these
            values are left at their defaults, the producer will override the
            defaults to be suitable. If the values are set to something
            incompatible with the idempotent producer, a KafkaConfigurationError
            will be raised.
        delivery_timeout_ms (float): An upper bound on the time to report success
            or failure after producer.send() returns. This limits the total time
            that a record will be delayed prior to sending, the time to await
            acknowledgement from the broker (if expected), and the time allowed
            for retriable send failures. The producer may report failure to send
            a record earlier than this config if either an unrecoverable error is
            encountered, the retries have been exhausted, or the record is added
            to a batch which reached an earlier delivery expiration deadline.
            The value of this config should be greater than or equal to the
            sum of (request_timeout_ms + linger_ms). Default: 120000.
        acks (0, 1, 'all'): The number of acknowledgments the producer requires
            the leader to have received before considering a request complete.
            This controls the durability of records that are sent. The
            following settings are common:

            0: Producer will not wait for any acknowledgment from the server.
                The message will immediately be added to the socket
                buffer and considered sent. No guarantee can be made that the
                server has received the record in this case, and the retries
                configuration will not take effect (as the client won't
                generally know of any failures). The offset given back for each
                record will always be set to -1.
            1: Wait for leader to write the record to its local log only.
                Broker will respond without awaiting full acknowledgement from
                all followers. In this case should the leader fail immediately
                after acknowledging the record but before the followers have
                replicated it then the record will be lost.
            all: Wait for the full set of in-sync replicas to write the record.
                This guarantees that the record will not be lost as long as at
                least one in-sync replica remains alive. This is the strongest
                available guarantee.
            If unset, defaults to acks=1.
        compression_type (str): The compression type for all data generated by
            the producer. Valid values are 'gzip', 'snappy', 'lz4', 'zstd' or None.
            Compression is of full batches of data, so the efficacy of batching
            will also impact the compression ratio (more batching means better
            compression). Default: None.
        retries (numeric): Setting a value greater than zero will cause the client
            to resend any record whose send fails with a potentially transient
            error. Note that this retry is no different than if the client
            resent the record upon receiving the error. Allowing retries
            without setting max_in_flight_requests_per_connection to 1 will
            potentially change the ordering of records because if two batches
            are sent to a single partition, and the first fails and is retried
            but the second succeeds, then the records in the second batch may
            appear first. Note additionally that produce requests will be
            failed before the number of retries has been exhausted if the timeout
            configured by delivery_timeout_ms expires first before successful
            acknowledgement. Users should generally prefer to leave this config
            unset and instead use delivery_timeout_ms to control retry behavior.
            Default: float('inf') (infinite)
        batch_size (int): Requests sent to brokers will contain multiple
            batches, one for each partition with data available to be sent.
            A small batch size will make batching less common and may reduce
            throughput (a batch size of zero will disable batching entirely).
            Default: 16384
        linger_ms (int): The producer groups together any records that arrive
            in between request transmissions into a single batched request.
            Normally this occurs only under load when records arrive faster
            than they can be sent out. However in some circumstances the client
            may want to reduce the number of requests even under moderate load.
            This setting accomplishes this by adding a small amount of
            artificial delay; that is, rather than immediately sending out a
            record the producer will wait for up to the given delay to allow
            other records to be sent so that the sends can be batched together.
            This can be thought of as analogous to Nagle's algorithm in TCP.
            This setting gives the upper bound on the delay for batching: once
            we get batch_size worth of records for a partition it will be sent
            immediately regardless of this setting, however if we have fewer
            than this many bytes accumulated for this partition we will
            'linger' for the specified time waiting for more records to show
            up. This setting defaults to 0 (i.e. no delay). Setting linger_ms=5
            would have the effect of reducing the number of requests sent but
            would add up to 5ms of latency to records sent in the absence of
            load. Default: 0.
        partitioner (callable): Callable used to determine which partition
            each message is assigned to. Called (after key serialization):
            partitioner(key_bytes, all_partitions, available_partitions).
            The default partitioner implementation hashes each non-None key
            using the same murmur2 algorithm as the java client so that
            messages with the same key are assigned to the same partition.
            When a key is None, the message is delivered to a random partition
            (filtered to partitions with available leaders only, if possible).
        connections_max_idle_ms: Close idle connections after the number of
            milliseconds specified by this config. The broker closes idle
            connections after connections.max.idle.ms, so this avoids hitting
            unexpected socket disconnected errors on the client.
            Default: 540000
        max_block_ms (int): Number of milliseconds to block during
            :meth:`~kafka.KafkaProducer.send` and
            :meth:`~kafka.KafkaProducer.partitions_for`. These methods can be
            blocked either because the buffer is full or metadata unavailable.
            Blocking in the user-supplied serializers or partitioner will not be
            counted against this timeout. Default: 60000.
        max_request_size (int): The maximum size of a request. This is also
            effectively a cap on the maximum record size. Note that the server
            has its own cap on record size which may be different from this.
            This setting will limit the number of record batches the producer
            will send in a single request to avoid sending huge requests.
            Default: 1048576.
        allow_auto_create_topics (bool): Enable/disable auto topic creation
            on metadata request. Only available with api_version >= (0, 11).
            Default: True
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        request_timeout_ms (int): Client request timeout in milliseconds.
            Default: 30000.
        receive_buffer_bytes (int): The size of the TCP receive buffer
            (SO_RCVBUF) to use when reading data. Default: None (relies on
            system defaults). Java client defaults to 32768.
        send_buffer_bytes (int): The size of the TCP send buffer
            (SO_SNDBUF) to use when sending data. Default: None (relies on
            system defaults). Java client defaults to 131072.
        socket_options (list): List of tuple-arguments to socket.setsockopt
            to apply to broker connection sockets. Default:
            [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
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
        max_in_flight_requests_per_connection (int): Requests are pipelined
            to kafka brokers up to this number of maximum requests per
            broker connection. Note that if this setting is set to be greater
            than 1 and there are failed sends, there is a risk of message
            re-ordering due to retries (i.e., if retries are enabled).
            Default: 5.
        security_protocol (str): Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
        ssl_context (ssl.SSLContext): pre-configured SSLContext for wrapping
            socket connections. If provided, all other ssl_* configurations
            will be ignored. Default: None.
        ssl_check_hostname (bool): flag to configure whether ssl handshake
            should verify that the certificate matches the brokers hostname.
            default: true.
        ssl_cafile (str): optional filename of ca file to use in certificate
            verification. default: none.
        ssl_certfile (str): optional filename of file in pem format containing
            the client certificate, as well as any ca certificates needed to
            establish the certificate's authenticity. default: none.
        ssl_keyfile (str): optional filename containing the client private key.
            default: none.
        ssl_password (str): optional password to be used when loading the
            certificate chain. default: none.
        ssl_crlfile (str): optional filename containing the CRL to check for
            certificate expiration. By default, no CRL check is done. When
            providing a file, only the leaf certificate will be checked against
            this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+.
            default: none.
        ssl_ciphers (str): optionally set the available ciphers for ssl
            connections. It should be a string in the OpenSSL cipher list
            format. If no cipher can be selected (because compile-time options
            or other configuration forbids use of all the specified ciphers),
            an ssl.SSLError will be raised. See ssl.SSLContext.set_ciphers
        api_version (tuple): Specify which Kafka API version to use. If set to
            None, the client will attempt to determine the broker version via
            ApiVersionsRequest API or, for brokers earlier than 0.10, probing
            various known APIs. Dynamic version checking is performed eagerly
            during __init__ and can raise NoBrokersAvailableError if no connection
            was made before timeout (see api_version_auto_timeout_ms below).
            Different versions enable different functionality.

            Examples:
                (3, 9) most recent broker release, enable all supported features
                (0, 11) enables message format v2 (internal)
                (0, 10, 0) enables sasl authentication and message format v1
                (0, 8, 0) enables basic functionality only

            Default: None
        api_version_auto_timeout_ms (int): number of milliseconds to throw a
            timeout exception from the constructor when checking the broker
            api version. Only applies if api_version set to None.
            Default: 2000
        metric_reporters (list): A list of classes to use as metrics reporters.
            Implementing the AbstractMetricsReporter interface allows plugging
            in classes that will be notified of new metric creation. Default: []
        metrics_enabled (bool): Whether to track metrics on this instance. Default True.
        metrics_num_samples (int): The number of samples maintained to compute
            metrics. Default: 2
        metrics_sample_window_ms (int): The maximum age in milliseconds of
            samples used to compute metrics. Default: 30000
        selector (selectors.BaseSelector): Provide a specific selector
            implementation to use for I/O multiplexing.
            Default: selectors.DefaultSelector
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
        socks5_proxy (str): Socks5 proxy URL. Default: None
        kafka_client (callable): Custom class / callable for creating KafkaClient instances

    Note:
        Configuration parameters are described in more detail at
        https://kafka.apache.org/0100/documentation/#producerconfigs
    """
    DEFAULT_CONFIG: Incomplete
    DEPRECATED_CONFIGS: Incomplete
    config: Incomplete
    def __init__(self, **configs: Unpack[_KafkaProducerConfig]) -> None: ...
    def bootstrap_connected(self):
        """Return True if the bootstrap is connected."""
        ...
    def __del__(self) -> None: ...
    def close(self, timeout: float | None = None, null_logger: bool = False) -> None:
        """
        Close this producer.

        Arguments:
            timeout (float, optional): timeout in seconds to wait for completion.
        """
        ...
    def partitions_for(self, topic: str) -> set[int]:
        """Returns set of all known partitions for the topic."""
        ...
    @classmethod
    def max_usable_produce_magic(cls, api_version): ...
    def init_transactions(self) -> None:
        """
        Needs to be called before any other methods when the transactional.id is set in the configuration.

        This method does the following:
          1. Ensures any transactions initiated by previous instances of the producer with the same
             transactional_id are completed. If the previous instance had failed with a transaction in
             progress, it will be aborted. If the last transaction had begun completion,
             but not yet finished, this method awaits its completion.
          2. Gets the internal producer id and epoch, used in all future transactional
             messages issued by the producer.

        Note that this method will raise KafkaTimeoutError if the transactional state cannot
        be initialized before expiration of `max_block_ms`.

        Retrying after a KafkaTimeoutError will continue to wait for the prior request to succeed or fail.
        Retrying after any other exception will start a new initialization attempt.
        Retrying after a successful initialization will do nothing.

        Raises:
            IllegalStateError: if no transactional_id has been configured
            AuthorizationError: fatal error indicating that the configured
                transactional_id is not authorized.
            KafkaError: if the producer has encountered a previous fatal error or for any other unexpected error
            KafkaTimeoutError: if the time taken for initialize the transaction has surpassed `max.block.ms`.
        """
        ...
    def begin_transaction(self) -> None:
        """
        Should be called before the start of each new transaction.

        Note that prior to the first invocation of this method,
        you must invoke `init_transactions()` exactly one time.

        Raises:
            ProducerFencedError if another producer is with the same
                transactional_id is active.
        """
        ...
    def send_offsets_to_transaction(
        self, offsets: Mapping[TopicPartition, OffsetAndMetadata], consumer_group_id: str
    ) -> None:
        """
        Sends a list of consumed offsets to the consumer group coordinator, and also marks
        those offsets as part of the current transaction. These offsets will be considered
        consumed only if the transaction is committed successfully.

        This method should be used when you need to batch consumed and produced messages
        together, typically in a consume-transform-produce pattern.

        Arguments:
            offsets ({TopicPartition: OffsetAndMetadata}): map of topic-partition -> offsets to commit
                as part of current transaction.
            consumer_group_id (str): Name of consumer group for offsets commit.

        Raises:
            IllegalStateError: if no transactional_id, or transaction has not been started.
            ProducerFencedError: fatal error indicating another producer with the same transactional_id is active.
            UnsupportedVersionError: fatal error indicating the broker does not support transactions (i.e. if < 0.11).
            UnsupportedForMessageFormatError: fatal error indicating the message format used for the offsets
                topic on the broker does not support transactions.
            AuthorizationError: fatal error indicating that the configured transactional_id is not authorized.
            KafkaErro:r if the producer has encountered a previous fatal or abortable error, or for any
                other unexpected error
        """
        ...
    def commit_transaction(self) -> None:
        """
        Commits the ongoing transaction.

        Raises: ProducerFencedError if another producer with the same
                transactional_id is active.
        """
        ...
    def abort_transaction(self) -> None:
        """
        Aborts the ongoing transaction.

        Raises: ProducerFencedError if another producer with the same
                transactional_id is active.
        """
        ...
    def send(
        self,
        topic: str,
        value: object = None,
        key: object = None,
        headers: Sequence[tuple[str, bytes]] | None = None,
        partition: int | None = None,
        timestamp_ms: int | None = None,
    ) -> FutureRecordMetadata:
        """
        Publish a message to a topic.

        Arguments:
            topic (str): topic where the message will be published
            value (optional): message value. Must be type bytes, or be
                serializable to bytes via configured value_serializer. If value
                is None, key is required and message acts as a 'delete'.
                See kafka compaction documentation for more details:
                https://kafka.apache.org/documentation.html#compaction
                (compaction requires kafka >= 0.8.1)
            partition (int, optional): optionally specify a partition. If not
                set, the partition will be selected using the configured
                'partitioner'.
            key (optional): a key to associate with the message. Can be used to
                determine which partition to send the message to. If partition
                is None (and producer's partitioner config is left as default),
                then messages with the same key will be delivered to the same
                partition (but if key is None, partition is chosen randomly).
                Must be type bytes, or be serializable to bytes via configured
                key_serializer.
            headers (optional): a list of header key value pairs. List items
                are tuples of str key and bytes value.
            timestamp_ms (int, optional): epoch milliseconds (from Jan 1 1970 UTC)
                to use as the message timestamp. Defaults to current time.

        Returns:
            FutureRecordMetadata: resolves to RecordMetadata

        Raises:
            KafkaTimeoutError: if unable to fetch topic metadata, or unable
                to obtain memory buffer prior to configured max_block_ms
            TypeError: if topic is not a string
            ValueError: if topic is invalid: must be chars (a-zA-Z0-9._-), and less than 250 length
            AssertionError: if KafkaProducer is closed, or key and value are both None
        """
        ...
    def flush(self, timeout: float | None = None) -> None:
        """
        Invoking this method makes all buffered records immediately available
        to send (even if linger_ms is greater than 0) and blocks on the
        completion of the requests associated with these records. The
        post-condition of :meth:`~kafka.KafkaProducer.flush` is that any
        previously sent record will have completed
        (e.g. Future.is_done() == True). A request is considered completed when
        either it is successfully acknowledged according to the 'acks'
        configuration for the producer, or it results in an error.

        Other threads can continue sending messages while one thread is blocked
        waiting for a flush call to complete; however, no guarantee is made
        about the completion of messages sent after the flush call begins.

        Arguments:
            timeout (float, optional): timeout in seconds to wait for completion.

        Raises:
            KafkaTimeoutError: failure to flush buffered records within the
                provided timeout
        """
        ...
    def metrics(self, raw: bool = False) -> dict[str, dict[str, object]] | dict[object, object] | None:
        """
        Get metrics on producer performance.

        This is ported from the Java Producer, for details see:
        https://kafka.apache.org/documentation/#producer_monitoring

        Warning:
            This is an unstable interface. It may change in future
            releases without warning.
        """
        ...
