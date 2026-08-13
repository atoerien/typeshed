"""
Hanging-transaction tooling mixin for KafkaAdminClient (KIP-664).

Exposes four wire APIs (ListTransactions, DescribeTransactions,
DescribeProducers, WriteTxnMarkers in admin abort mode) plus the
``find_hanging_transactions`` convenience that ties them together,
mirroring the Java tool's ``kafka-transactions.sh --find-hanging``.
"""

import sys
from _typeshed import Incomplete
from typing import NamedTuple

from kafka.structs import TopicPartition
from kafka.util import EnumHelper

if sys.version_info >= (3, 11):
    from enum import StrEnum

    class TransactionState(EnumHelper, StrEnum):
        """
        Broker-reported transaction states (DescribeTransactions /
        ListTransactions wire values).
        """
        EMPTY = "Empty"
        ONGOING = "Ongoing"
        PREPARE_COMMIT = "PrepareCommit"
        PREPARE_ABORT = "PrepareAbort"
        COMPLETE_COMMIT = "CompleteCommit"
        COMPLETE_ABORT = "CompleteAbort"
        DEAD = "Dead"
        PREPARE_EPOCH_FENCE = "PrepareEpochFence"
        UNKNOWN = "Unknown"

else:
    from enum import Enum

    class TransactionState(EnumHelper, str, Enum):
        """
        Broker-reported transaction states (DescribeTransactions /
        ListTransactions wire values).
        """
        EMPTY = "Empty"
        ONGOING = "Ongoing"
        PREPARE_COMMIT = "PrepareCommit"
        PREPARE_ABORT = "PrepareAbort"
        COMPLETE_COMMIT = "CompleteCommit"
        COMPLETE_ABORT = "CompleteAbort"
        DEAD = "Dead"
        PREPARE_EPOCH_FENCE = "PrepareEpochFence"
        UNKNOWN = "Unknown"

class TransactionListing(NamedTuple):
    """One row from a ListTransactions response."""
    transactional_id: str
    producer_id: int
    state: TransactionState

class TransactionDescription(NamedTuple):
    """
    One transactional id's state as returned by DescribeTransactions,
    plus the coordinator that owns it.
    """
    coordinator_id: int
    state: TransactionState
    producer_id: int
    producer_epoch: int
    transaction_timeout_ms: int
    transaction_start_time_ms: int
    topic_partitions: set[TopicPartition]

class ProducerState(NamedTuple):
    """One ActiveProducer row from DescribeProducers."""
    producer_id: int
    producer_epoch: int
    last_sequence: int
    last_timestamp: int
    coordinator_epoch: int
    current_transaction_start_offset: int

class PartitionProducerState(NamedTuple):
    """PartitionProducerState(active_producers,)"""
    active_producers: list[ProducerState]

class AbortTransactionSpec(NamedTuple):
    """
    Inputs for ``abort_transaction``. ``coordinator_epoch=-1`` is the
    sentinel used by the Java admin tool to bypass the epoch check; the
    partition leader still validates ``producer_id``/``producer_epoch``
    against current state.
    """
    topic_partition: TopicPartition
    producer_id: int
    producer_epoch: int
    coordinator_epoch: int = -1

class TransactionsAdminMixin:
    """Mixin providing KIP-664 hanging-transaction tooling."""
    config: dict[Incomplete, Incomplete]
    def list_transactions(
        self,
        broker_ids=None,
        producer_id_filters=None,
        state_filters=None,
        duration_filter_ms: float | None = None,
        transactional_id_pattern: str | None = None,
    ):
        """
        List active transactions across all brokers (or a subset).

        Each broker hosts a slice of the ``__transaction_state`` topic,
        so a full listing requires sharding the request to every broker
        and concatenating the results.

        Keyword Arguments:
            broker_ids ([int], optional): Brokers to query. Default: every
                broker in the cluster metadata.
            producer_id_filters ([int], optional): Only return transactions
                whose ``producer_id`` is in this list.
            state_filters ([str], optional): Only return transactions whose
                broker-reported state matches. Accepts :class:`TransactionState`
                members or their string wire values.
            duration_filter_ms (int, optional): Only return transactions
                running longer than this. Requires broker >= 3.8
                (ListTransactions v1+).
            transactional_id_pattern (str, optional): Only return
                transactions whose transactional id matches this regex.
                Requires broker >= 4.1 (ListTransactions v2+, KIP-1152).

        Returns:
            dict: A dict mapping broker ``node_id`` to a list of
            :class:`TransactionListing`.
        """
        ...
    def describe_transactions(self, transactional_ids):
        """
        Describe one or more transactions by transactional id.

        Each request is routed to the transaction coordinator that owns
        the transactional id (discovered via FindCoordinator with
        ``CoordinatorType.TRANSACTION``).

        Arguments:
            transactional_ids: Iterable of transactional id strings.

        Returns:
            dict: A dict mapping ``transactional_id`` (str) to
            :class:`TransactionDescription`.

        Raises:
            TransactionalIdNotFoundError: If a transactional id is unknown
                to its coordinator.
            BrokerResponseError: For any other per-id error.
        """
        ...
    def describe_producers(self, partitions, broker_id: int | None = None):
        """
        Describe active producer state on a set of topic partitions.

        Arguments:
            partitions: Iterable of :class:`~kafka.TopicPartition`.

        Keyword Arguments:
            broker_id (int, optional): Replica to query. Default: the
                partition leader (discovered from cluster metadata).

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to
            :class:`PartitionProducerState`.

        Raises:
            BrokerResponseError: For any per-partition error (e.g.
                ``NotLeaderOrFollowerError`` if the chosen broker is not
                a replica).
        """
        ...
    def abort_transaction(self, spec):
        """
        Administratively abort an open transaction on a partition.

        Sends a WriteTxnMarkers request (with ``transaction_result=False``)
        to the partition leader. The leader validates ``producer_id`` /
        ``producer_epoch`` against current state before writing the
        abort marker. Pass ``coordinator_epoch=-1`` (the default) to
        signal an admin abort that bypasses the coordinator-epoch
        guard, matching the Java AdminClient behaviour.

        Arguments:
            spec (:class:`AbortTransactionSpec`): Target partition,
                producer id/epoch, and optional coordinator epoch.
        """
        ...
    def find_hanging_transactions(self, broker_ids=None, max_transaction_timeout_ms: float = 900000):
        """
        Detect transactions whose age exceeds the broker timeout + 5min.

        Convenience wrapper that runs :meth:`list_transactions` against
        each broker, then :meth:`describe_transactions` to read
        ``transaction_start_time_ms``, and filters to transactions in an
        active state whose age exceeds the threshold. Mirrors
        ``kafka-transactions.sh --find-hanging``.

        Keyword Arguments:
            broker_ids ([int], optional): Brokers to query. Default: all.
            max_transaction_timeout_ms (int): Suspected-hang threshold.
                Default: 900000 (15 minutes -- Kafka's default
                ``transaction.max.timeout.ms``).

        Returns:
            list: One dict per suspected hanging transaction with keys
            ``transactional_id``, ``producer_id``, ``producer_epoch``,
            ``state``, ``age_ms``, ``coordinator_id``,
            ``topic_partitions``.
        """
        ...
