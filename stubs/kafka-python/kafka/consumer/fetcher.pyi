from _typeshed import Incomplete
from typing import ClassVar, NamedTuple

import kafka.errors as Errors

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

class RecordTooLargeError(Errors.KafkaError): ...

class Fetcher:
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    def __init__(self, client, subscriptions, **configs) -> None: ...
    def fetch_records(self, max_records: int | None = None, update_offsets: bool = True, timeout_ms=None): ...
    def send_fetches(self): ...
    def in_flight_fetches(self) -> bool: ...
    def reset_offsets_if_needed(self, timeout_ms=None): ...
    def offsets_by_times(self, timestamps, timeout_ms=None): ...
    def beginning_offsets(self, partitions, timeout_ms=None): ...
    def end_offsets(self, partitions, timeout_ms=None): ...
    def beginning_or_end_offset(self, partitions, timestamp, timeout_ms=None): ...
    def fetched_records(self, max_records: int | None = None, update_offsets: bool = True): ...
    def maybe_validate_positions(self) -> None: ...
    def validate_offsets_if_needed(self, timeout_ms=None): ...
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
