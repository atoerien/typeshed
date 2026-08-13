from _typeshed import Incomplete
from typing import ClassVar, NamedTuple

import kafka.errors as Errors

class ConsumerRecord(NamedTuple):
    """
    A single record (message) consumed from a topic partition.

    Yielded by :meth:`~kafka.KafkaConsumer.poll` (inside the returned
    ``{TopicPartition: [ConsumerRecord, ...]}`` mapping) and by iterating
    over a :class:`~kafka.KafkaConsumer`. ``key`` and ``value`` are decoded
    by the consumer's configured deserializers.

    Keyword Arguments:
        topic (str): The topic this record was received from.
        partition (int): The partition this record was received from.
        leader_epoch (int): The partition leader epoch for this record, or -1
            if unknown.
        offset (int): The position of this record in the topic partition.
        timestamp (int): The timestamp of this record, in milliseconds since
            the epoch (UTC), or -1 if unknown.
        timestamp_type (int): The type of the timestamp: 0 for CreateTime (set
            by the producer) or 1 for LogAppendTime (set by the broker).
        key: The (deserialized) key of the record, or None.
        value: The (deserialized) value of the record, or None.
        headers (list): A list of ``(key, value)`` header tuples, where key is
            a str and value is bytes.
        checksum (int): Deprecated. The CRC32 checksum of the record, or None.
            Removed in message format v2 (Kafka 0.11+).
        serialized_key_size (int): The size of the serialized, uncompressed key
            in bytes, or -1 if the key is None.
        serialized_value_size (int): The size of the serialized, uncompressed
            value in bytes, or -1 if the value is None.
        serialized_header_size (int): The size of the serialized, uncompressed
            headers in bytes, or -1 if there are no headers.
    """
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

class RecordTooLargeError(Errors.KafkaError): ...

class Fetcher:
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    def __init__(self, client, subscriptions, **configs) -> None:
        """
        Initialize a Kafka Message Fetcher.

        Keyword Arguments:
            key_deserializer (kafka.serializer.Deserializer): Takes a
                raw message key and returns a deserialized key.
                Default: None.
            value_deserializer (kafka.serializer.Deserializer): Takes a
                raw message value and returns a deserialized value.
                Default: None.
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
    def fetch_records(self, max_records: int | None = None, update_offsets: bool = True, timeout_ms=None):
        """
        Drain buffered records, pipeline next fetches, and wait briefly
        for in-flight responses if no records are immediately available.

        Single-call replacement for the legacy
        ``fetched_records -> send_fetches -> client.poll -> fetched_records``
        loop in :meth:`KafkaConsumer._poll_once`. The caller no longer
        drives the event loop; the wait happens inside this method via a
        wakeup Future fired by any in-flight fetch's completion callback.

        Arguments:
            max_records (int, optional): cap on returned records.
            update_offsets (bool): advance subscription positions for
                consumed records.
            timeout_ms (int, optional): wall-clock cap on the wait phase.
                Only applies when no records are immediately available.

        Returns:
            tuple[dict[TopicPartition, list[ConsumerRecord]], bool]:
                ``(records, idle)``. ``idle`` is True when there were no
                buffered records, no in-flight fetches, and no pending
                offset-reset task -- i.e. nothing this fetcher could wait
                on. Callers in that state should sleep before retrying
                instead of busy-looping.
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
    def in_flight_fetches(self) -> bool:
        """
        Return True if there are any unprocessed (incomplete) FetchRequests
        in flight.
        """
        ...
    def reset_offsets_if_needed(self, timeout_ms=None):
        """
        Schedule pending offset resets and return the in-flight Task.

        Returns the cached Future for the in-flight reset task (shared
        across concurrent callers) or None if no reset is needed. Callers
        may discard the Future (fire-and-forget, e.g. consumer.poll) or
        await it via ``manager.wait_for(future, timeout_ms)`` to block
        until resets complete (e.g. consumer.position).

        Arguments:
            timeout_ms (int, optional): Maximum wall-clock the reset task
                should run, including time spent awaiting metadata refresh
                for unknown leaders. If None, uses ``request_timeout_ms``
                as a default upper bound so a permanently-unresolvable
                partition (deleted topic, etc.) doesn't spin forever. The
                first caller's timeout wins for the cached task; later
                callers' bounds are enforced via their own ``wait_for`` on
                the returned Future.

        Raises:
            NoOffsetForPartitionError: if a previous reset attempt left a
                cached non-retriable exception.
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
            {TopicPartition: OffsetAndTimestamp or None}: Mapping of partition to
                retrieved offset, timestamp, and leader_epoch. If offset does not
                exist for the provided timestamp, the value for the TopicPartition
                will be None.

        Raises:
            KafkaTimeoutError if timeout_ms provided
        """
        ...
    def beginning_offsets(self, partitions, timeout_ms=None):
        """
        Fetch earliest (oldest) offset for each partition.

        Blocks until offsets are obtained, a non-retriable exception is raised
        or ``timeout_ms`` passed.

        Arguments:
            partitions ([TopicPartition]): List of partitions for list offsets.
            timeout_ms (int, optional): The maximum time in milliseconds to block.

        Returns:
            {TopicPartition: int}: Mapping of partition to retrieved offset.

        Raises:
            KafkaTimeoutError if timeout_ms provided.
        """
        ...
    def end_offsets(self, partitions, timeout_ms=None):
        """
        Fetch latest (most recent) offset for each partition.

        Blocks until offsets are obtained, a non-retriable exception is raised
        or ``timeout_ms`` passed.

        Arguments:
            partitions ([TopicPartition]): List of partitions for list offsets.
            timeout_ms (int, optional): The maximum time in milliseconds to block.

        Returns:
            {TopicPartition: int}: Mapping of partition to retrieved offset.

        Raises:
            KafkaTimeoutError if timeout_ms provided.
        """
        ...
    def beginning_or_end_offset(self, partitions, timestamp, timeout_ms=None):
        """
        Fetch offset for each partition using ``timestamp``.

        Blocks until offsets are obtained, a non-retriable exception is raised
        or ``timeout_ms`` passed.

        Arguments:
            partitions ([TopicPartition]): List of partitions for list offsets.
            timestamp (int or OffsetSpec): OffsetSpec.LATEST (-1) for the latest
                available, OffsetSpec.EARLIEST (-2) for the earliest available.
                Otherwise timestamp is treated as epoch milliseconds.
            timeout_ms (int, optional): The maximum time in milliseconds to block.

        Returns:
            {TopicPartition: int}: Mapping of partition to retrieved offset.

        Raises:
            UnsupportedVersionError if broker does not support any compatible
                ListOffsetsRequest api version.
            KafkaTimeoutError if timeout_ms provided.
        """
        ...
    def fetched_records(self, max_records: int | None = None, update_offsets: bool = True):
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
            ValueError: if max_records is <= 0

        Returns: (records (dict), partial (bool))
            records: {TopicPartition: [messages]}
            partial: True if records returned did not fully drain any pending
                partition requests. This may be useful for choosing when to
                pipeline additional fetch requests.
        """
        ...
    def maybe_validate_positions(self) -> None:
        """
        Walk assigned partitions; mark any whose cluster leader epoch has
        advanced beyond the position's epoch as awaiting validation.

        Cheap fire-and-forget marker; the actual RPC fan-out runs in
        ``validate_offsets_if_needed`` -> ``_validate_offsets_async``.
        Idempotent: partitions already awaiting validation, awaiting
        reset, or with no recorded epoch are skipped inside
        ``maybe_validate_position``.
        """
        ...
    def validate_offsets_if_needed(self, timeout_ms=None):
        """
        Schedule any pending position validations and return the in-flight Task.

        Mirrors :meth:`reset_offsets_if_needed`: returns a cached Future
        shared across callers so concurrent ``consumer.poll`` and
        ``consumer.position`` callers don't race the same partition into
        duplicate OffsetForLeaderEpoch requests.

        Raises:
            LogTruncationError: if a previous validation detected truncation
                on one or more partitions. The exception is cleared after
                being raised so subsequent calls will re-attempt validation.
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
            isolation_level=...,
            aborted_transactions=None,
            metric_aggregator=None,
            on_drain=...,
        ) -> None: ...
        def __bool__(self) -> bool: ...
        def drain(self) -> None: ...
        def take(self, n=None) -> list[Incomplete]: ...

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
    __slots__ = ("session_id", "epoch")
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
    __slots__ = ("_to_send", "_to_forget", "_metadata")
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
    __slots__ = ("total_bytes", "total_records")
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
