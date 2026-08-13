"""
KIP-480 sticky partitioner.

Records with a non-None key are hashed to a partition just like
:class:`~kafka.partitioner.default.DefaultPartitioner`. Records with a
None key go to a *sticky* partition - i.e. the same partition is reused
for every null-key record on a topic until KafkaProducer signals that a
batch has been completed (via :meth:`StickyPartitioner.on_new_batch`),
at which point a different partition is picked.

The goal is to give the RecordAccumulator larger, denser batches for
null-key sends so per-batch overhead (CRC, compression, broker
round-trip) is amortized across more records. Java's benchmark in
KIP-480 reported substantial throughput/latency improvements over the
default-random behavior, though kafka-python is unlikely to see similar
improvements while predominantly CPU-bound on per-record overhead.
"""

from .default import DefaultPartitioner

class StickyPartitioner(DefaultPartitioner):
    """
    Partitioner that sticks null-key records to one partition per
    topic until ``on_new_batch`` rotates it.

    Thread-safety: ``_sticky`` mutations are protected by ``_lock`` so
    concurrent ``send()`` callers can't observe a torn read-modify-write.
    """
    def __init__(self) -> None: ...
    def partition(self, topic, key, serialized_key, value, serialized_value, cluster):
        """
        Choose a partition for the next record.

        Arguments:
            topic (str): topic to partition on.
            key (any): Unserialized key.
            serialized_key (bytes or None): partitioning key.
            value (any): Unserialized value.
            serialized_value (bytes or None): serialized value.
            cluster (ClusterMetadata): metadata for cluster; provides
                all and available partitions for topic.

        Raises:
            ValueError: if topic is not in ClusterMetadata

        Returns:
            int: chosen partition ID.
        """
        ...
    def on_new_batch(self, topic, cluster, prev_partition) -> None:
        """
        Hook called by ``KafkaProducer`` on the abort-for-new-batch
        retry path: rotate the sticky for ``topic`` so the next
        null-key record lands on a different partition.

        Stale events (where another thread already rotated us off
        ``prev_partition``) are no-ops.
        """
        ...
