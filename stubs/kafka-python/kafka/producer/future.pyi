from _typeshed import Incomplete
from typing import NamedTuple

from kafka.future import Future
from kafka.structs import TopicPartition

class FutureProduceResult(Future):
    __slots__ = ("topic_partition", "_latch")
    topic_partition: TopicPartition
    def __init__(self, topic_partition: TopicPartition) -> None: ...
    def success(self, value): ...
    def failure(self, error): ...
    def wait(self, timeout=None): ...

class FutureRecordMetadata(Future):
    """
    An asynchronous handle to the result of a single :meth:`~kafka.KafkaProducer.send`.

    :meth:`~kafka.KafkaProducer.send` returns one of these immediately,
    before the record has been transmitted to the broker. Call :meth:`get`
    to block until the record is acknowledged and obtain its
    :class:`RecordMetadata`, or register callbacks via
    :meth:`~kafka.future.Future.add_callback` /
    :meth:`~kafka.future.Future.add_errback` to be notified without
    blocking. The future resolves successfully once the containing batch is
    acknowledged according to the producer's ``acks`` configuration, or
    fails with the relevant exception (for example
    :class:`~kafka.errors.KafkaTimeoutError`).
    """
    __slots__ = ("_produce_future", "args")
    args: Incomplete
    def __init__(
        self,
        produce_future,
        batch_index,
        timestamp_ms,
        checksum,
        serialized_key_size,
        serialized_value_size,
        serialized_header_size,
    ) -> None: ...
    def rebind(self, new_produce_future, new_batch_index) -> None:
        """
        Rebind this future to a new produce future with a new batch index.

        Used when a batch is split due to MESSAGE_TOO_LARGE. The original
        FutureRecordMetadata is rebound to the new (smaller) batch's future.

        This must be called from the sender thread while the old produce_future
        has not been completed. Any user thread blocked in get() on the old
        produce_future's latch will be woken and will re-wait on the new one.
        """
        ...
    def get(self, timeout=None):
        """Wait for up to timeout seconds for future to complete."""
        ...

class RecordMetadata(NamedTuple):
    """
    Metadata about a record that has been acknowledged by the broker.

    Returned by :meth:`FutureRecordMetadata.get`, which resolves once the
    batch containing the record has been acknowledged according to the
    producer's ``acks`` configuration.

    Keyword Arguments:
        topic (str): The topic the record was appended to.
        partition (int): The partition the record was appended to.
        topic_partition (TopicPartition): The ``(topic, partition)`` the record
            was appended to.
        offset (int): The offset of the record in the topic partition, or -1 if
            the broker did not assign one (e.g. ``acks=0``).
        timestamp (int): The timestamp of the record, in milliseconds since the
            epoch (UTC). For CreateTime this is the producer-supplied timestamp;
            for LogAppendTime it is the broker-assigned timestamp.
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
    topic_partition: TopicPartition
    offset: int
    timestamp: int
    checksum: int | None  # Deprecated field
    serialized_key_size: int
    serialized_value_size: int
    serialized_header_size: int
