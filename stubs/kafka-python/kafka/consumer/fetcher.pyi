from _typeshed import Incomplete
from typing import ClassVar, NamedTuple

import kafka.errors as Errors

log: Incomplete
READ_UNCOMMITTED: int
READ_COMMITTED: int
ISOLATION_LEVEL_CONFIG: Incomplete

class ConsumerRecord(NamedTuple):
    """ConsumerRecord(topic, partition, leader_epoch, offset, timestamp, timestamp_type, key, value, headers, checksum, serialized_key_size, serialized_value_size, serialized_header_size)"""
    topic: str
    partition: int
    leader_epoch: int | None
    offset: int
    timestamp: int
    timestamp_type: int
    key: Incomplete
    value: Incomplete
    headers: list[tuple[str, bytes]]
    checksum: int | None
    serialized_key_size: int
    serialized_value_size: int
    serialized_header_size: int

class CompletedFetch(NamedTuple):
    """CompletedFetch(topic_partition, fetched_offset, response_version, partition_data, metric_aggregator)"""
    topic_partition: Incomplete
    fetched_offset: Incomplete
    response_version: Incomplete
    partition_data: Incomplete
    metric_aggregator: Incomplete

class ExceptionMetadata(NamedTuple):
    """ExceptionMetadata(partition, fetched_offset, exception)"""
    partition: Incomplete
    fetched_offset: Incomplete
    exception: Incomplete

class NoOffsetForPartitionError(Errors.KafkaError): ...
class RecordTooLargeError(Errors.KafkaError): ...

class Fetcher:
    DEFAULT_CONFIG: Incomplete
    config: Incomplete
    def __init__(self, client, subscriptions, **configs) -> None:
        """
        Initialize a Kafka Message Fetcher.

        Keyword Arguments:
            key_deserializer (callable): Any callable that takes a
                raw message key and returns a deserialized key.
            value_deserializer (callable, optional): Any callable that takes a
                raw message value and returns a deserialized value.
            enable_incremental_fetch_sessions: (bool): Use incremental fetch sessions
                when available / supported by kafka broker. See KIP-227. Default: True.
            fetch_min_bytes (int): Minimum amount of data the server should
                return for a fetch request, otherwise wait up to
                fetch_max_wait_ms for more data to accumulate. Default: 1.
            fetch_max_wait_ms (int): The maximum amount of time in milliseconds
                the server will block before answering the fetch request if
                there isn't sufficient data to immediately satisfy the
                requirement given by fetch_min_bytes. Default: 500.
            fetch_max_bytes (int): The maximum amount of data the server should
                return for a fetch request. This is not an absolute maximum, if
                the first message in the first non-empty partition of the fetch
                is larger than this value, the message will still be returned
                to ensure that the consumer can make progress. NOTE: consumer
                performs fetches to multiple brokers in parallel so memory
                usage will depend on the number of brokers containing
                partitions for the topic.
                Supported Kafka version >= 0.10.1.0. Default: 52428800 (50 MB).
            max_partition_fetch_bytes (int): The maximum amount of data
                per-partition the server will return. The maximum total memory
                used for a request = #partitions * max_partition_fetch_bytes.
                This size must be at least as large as the maximum message size
                the server allows or else it is possible for the producer to
                send messages larger than the consumer can fetch. If that
                happens, the consumer can get stuck trying to fetch a large
                message on a certain partition. Default: 1048576.
            check_crcs (bool): Automatically check the CRC32 of the records
                consumed. This ensures no on-the-wire or on-disk corruption to
                the messages occurred. This check adds some overhead, so it may
                be disabled in cases seeking extreme performance. Default: True
            isolation_level (str): Configure KIP-98 transactional consumer by
                setting to 'read_committed'. This will cause the consumer to
                skip records from aborted tranactions. Default: 'read_uncommitted'
        """
        ...
    def send_fetches(self):
        """
        Send FetchRequests for all assigned partitions that do not already have
        an in-flight fetch or pending fetch data.

        Returns:
            List of Futures: each future resolves to a FetchResponse
        """
        ...
    def in_flight_fetches(self):
        """Return True if there are any unprocessed FetchRequests in flight."""
        ...
    def reset_offsets_if_needed(self):
        """
        Reset offsets for the given partitions using the offset reset strategy.

        Arguments:
            partitions ([TopicPartition]): the partitions that need offsets reset

        Returns:
            bool: True if any partitions need reset; otherwise False (no reset pending)

        Raises:
            NoOffsetForPartitionError: if no offset reset strategy is defined
            KafkaTimeoutError if timeout_ms provided
        """
        ...
    def offsets_by_times(self, timestamps, timeout_ms=None):
        """
        Fetch offset for each partition passed in ``timestamps`` map.

        Blocks until offsets are obtained, a non-retriable exception is raised
        or ``timeout_ms`` passed.

        Arguments:
            timestamps: {TopicPartition: int} dict with timestamps to fetch
                offsets by. -1 for the latest available, -2 for the earliest
                available. Otherwise timestamp is treated as epoch milliseconds.
            timeout_ms (int, optional): The maximum time in milliseconds to block.

        Returns:
            {TopicPartition: OffsetAndTimestamp}: Mapping of partition to
                retrieved offset, timestamp, and leader_epoch. If offset does not exist for
                the provided timestamp, that partition will be missing from
                this mapping.

        Raises:
            KafkaTimeoutError if timeout_ms provided
        """
        ...
    def beginning_offsets(self, partitions, timeout_ms): ...
    def end_offsets(self, partitions, timeout_ms): ...
    def beginning_or_end_offset(self, partitions, timestamp, timeout_ms): ...
    def fetched_records(self, max_records=None, update_offsets: bool = True):
        """
        Returns previously fetched records and updates consumed offsets.

        Arguments:
            max_records (int): Maximum number of records returned. Defaults
                to max_poll_records configuration.

        Raises:
            OffsetOutOfRangeError: if no subscription offset_reset_strategy
            CorruptRecordError: if message crc validation fails (check_crcs
                must be set to True)
            RecordTooLargeError: if a message is larger than the currently
                configured max_partition_fetch_bytes
            TopicAuthorizationError: if consumer is not authorized to fetch
                messages from the topic

        Returns: (records (dict), partial (bool))
            records: {TopicPartition: [messages]}
            partial: True if records returned did not fully drain any pending
                partition requests. This may be useful for choosing when to
                pipeline additional fetch requests.
        """
        ...
    def close(self) -> None: ...

    class PartitionRecords:
        fetch_offset: Incomplete
        topic_partition: Incomplete
        leader_epoch: int
        next_fetch_offset: Incomplete
        bytes_read: int
        records_read: int
        isolation_level: Incomplete
        aborted_producer_ids: Incomplete
        aborted_transactions: Incomplete
        metric_aggregator: Incomplete
        check_crcs: Incomplete
        record_iterator: Incomplete
        on_drain: Incomplete
        def __init__(
            self,
            fetch_offset,
            tp,
            records,
            key_deserializer=None,
            value_deserializer=None,
            check_crcs: bool = True,
            isolation_level=0,
            aborted_transactions=None,
            metric_aggregator=None,
            on_drain=...,
        ) -> None: ...
        def __bool__(self) -> bool: ...
        __nonzero__ = __bool__
        def drain(self) -> None: ...
        def take(self, n=None): ...

class FetchSessionHandler:
    """
    FetchSessionHandler maintains the fetch session state for connecting to a broker.

    Using the protocol outlined by KIP-227, clients can create incremental fetch sessions.
    These sessions allow the client to fetch information about a set of partition over
    and over, without explicitly enumerating all the partitions in the request and the
    response.

    FetchSessionHandler tracks the partitions which are in the session.  It also
    determines which partitions need to be included in each fetch request, and what
    the attached fetch session metadata should be for each request.
    """
    node_id: Incomplete
    next_metadata: Incomplete
    session_partitions: Incomplete
    def __init__(self, node_id) -> None: ...
    def build_next(self, next_partitions):
        """
        Arguments:
            next_partitions (dict): TopicPartition -> TopicPartitionState

        Returns:
            FetchRequestData
        """
        ...
    def handle_response(self, response): ...
    def handle_error(self, _exception) -> None: ...

class FetchMetadata:
    MAX_EPOCH: int
    INVALID_SESSION_ID: int
    THROTTLED_SESSION_ID: int
    INITIAL_EPOCH: int
    FINAL_EPOCH: int
    INITIAL: ClassVar[FetchMetadata]
    LEGACY: ClassVar[FetchMetadata]
    session_id: Incomplete
    epoch: Incomplete
    def __init__(self, session_id, epoch) -> None: ...
    @property
    def is_full(self): ...
    @classmethod
    def next_epoch(cls, prev_epoch): ...
    def next_close_existing(self): ...
    @classmethod
    def new_incremental(cls, session_id): ...
    def next_incremental(self): ...

class FetchRequestData:
    def __init__(self, to_send, to_forget, metadata) -> None: ...
    @property
    def metadata(self): ...
    @property
    def id(self): ...
    @property
    def epoch(self): ...
    @property
    def to_send(self): ...
    @property
    def to_forget(self): ...

class FetchMetrics:
    total_bytes: int
    total_records: int
    def __init__(self) -> None: ...

class FetchResponseMetricAggregator:
    """
    Since we parse the message data for each partition from each fetch
    response lazily, fetch-level metrics need to be aggregated as the messages
    from each partition are parsed. This class is used to facilitate this
    incremental aggregation.
    """
    sensors: Incomplete
    unrecorded_partitions: Incomplete
    fetch_metrics: Incomplete
    topic_fetch_metrics: Incomplete
    def __init__(self, sensors, partitions) -> None: ...
    def record(self, partition, num_bytes, num_records) -> None:
        """
        After each partition is parsed, we update the current metric totals
        with the total bytes and number of records parsed. After all partitions
        have reported, we write the metric.
        """
        ...

class FetchManagerMetrics:
    metrics: Incomplete
    group_name: Incomplete
    bytes_fetched: Incomplete
    records_fetched: Incomplete
    fetch_latency: Incomplete
    records_fetch_lag: Incomplete
    def __init__(self, metrics, prefix) -> None: ...
    def record_topic_fetch_metrics(self, topic, num_bytes, num_records) -> None: ...
