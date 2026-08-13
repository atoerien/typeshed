import selectors
import ssl
from _typeshed import Incomplete
from collections.abc import Callable, Mapping, Sequence
from types import TracebackType
from typing import Literal, TypeAlias
from typing_extensions import Self

from kafka.producer.future import FutureRecordMetadata
from kafka.producer.record_accumulator import AtomicInteger
from kafka.serializer.abstract import Serializer
from kafka.structs import ConsumerGroupMetadata, OffsetAndMetadata, TopicPartition

_Partitioner: TypeAlias = Callable[[bytes | None, Sequence[int], Sequence[int]], int]
_ProducerSerializer: TypeAlias = Serializer | Callable[[object], bytes]

PRODUCER_CLIENT_ID_SEQUENCE: AtomicInteger

class KafkaProducer:
    DEFAULT_CONFIG: dict[str, Incomplete]
    DEPRECATED_CONFIGS: tuple[str, ...]
    config: dict[str, Incomplete]
    def __init__(
        self,
        *,
        bootstrap_servers: str | Sequence[str] = "localhost",
        client_id: str | None = None,
        key_serializer: _ProducerSerializer | None = None,
        value_serializer: _ProducerSerializer | None = None,
        enable_idempotence: bool = True,
        transactional_id: str | None = None,
        transaction_timeout_ms: int = 60000,
        delivery_timeout_ms: float = 120000,
        acks: int | Literal["all"] = -1,
        compression_type: Literal["gzip", "snappy", "lz4", "zstd"] | None = None,
        retries: int | float = ...,
        batch_size: int = 16384,
        linger_ms: int = 0,
        partitioner: _Partitioner = ...,
        connections_max_idle_ms: int = 540000,
        max_block_ms: int = 60000,
        max_request_size: int = 1048576,
        allow_auto_create_topics: bool = True,
        metadata_max_age_ms: int = 300000,
        client_dns_lookup: str = "use_all_dns_ips",
        retry_backoff_ms: int = 100,
        request_timeout_ms: int = 30000,
        receive_message_max_bytes: int = 100_000_000,
        receive_buffer_bytes: int | None = None,
        send_buffer_bytes: int | None = None,
        socket_options: Sequence[tuple[int, int, int]] = ...,
        reconnect_backoff_ms: int = 50,
        reconnect_backoff_max_ms: int = 30000,
        max_in_flight_requests_per_connection: int = 5,
        security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT",
        ssl_context: ssl.SSLContext | None = None,
        ssl_check_hostname: bool = True,
        ssl_cafile: str | None = None,
        ssl_certfile: str | None = None,
        ssl_keyfile: str | None = None,
        ssl_crlfile: str | None = None,
        ssl_password: str | None = None,
        ssl_ciphers: str | None = None,
        api_version: tuple[int, ...] | None = None,
        bootstrap_timeout_ms: int = 30000,
        metric_reporters: Sequence[type[object]] = [],
        metrics_enabled: bool = True,
        metrics_num_samples: int = 2,
        metrics_sample_window_ms: int = 30000,
        selector: type[selectors.BaseSelector] = selectors.DefaultSelector,
        sasl_mechanism: Literal["PLAIN", "GSSAPI", "OAUTHBEARER", "SCRAM-SHA-256", "SCRAM-SHA-512"] | None = None,
        sasl_plain_username: str | None = None,
        sasl_plain_password: str | None = None,
        sasl_kerberos_name: object | None = None,
        sasl_kerberos_service_name: str = "kafka",
        sasl_kerberos_domain_name: str | None = None,
        sasl_oauth_token_provider: object | None = None,
        proxy_url: str | None = None,
        socks5_proxy: str | None = None,
        kafka_client: Callable[..., object] = ...,
    ) -> None: ...
    def bootstrap_connected(self) -> bool: ...
    def __del__(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def close(self, timeout: float | None = None, null_logger: bool = False) -> None: ...
    def partitions_for(self, topic: str) -> set[int]: ...
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
        self, offsets: Mapping[TopicPartition, OffsetAndMetadata], group_metadata: str | ConsumerGroupMetadata
    ) -> None: ...
    def commit_transaction(self) -> None: ...
    def abort_transaction(self) -> None: ...
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
