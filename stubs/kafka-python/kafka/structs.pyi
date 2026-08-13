"""Other useful structs """

from typing import Final, Literal, NamedTuple

class TopicPartition(NamedTuple):
    """
    A topic and partition tuple

    Keyword Arguments:
        topic (str): A topic name
        partition (int): A partition id
    """
    topic: str
    partition: int

class TopicPartitionReplica(NamedTuple):
    """
    A topic / partition / broker replica tuple

    Keyword Arguments:
        topic (str): A topic name
        partition (int): A partition id
        broker_id (int): The node_id of the broker hosting the replica
    """
    topic: str
    partition: int
    broker_id: int

class OffsetAndMetadata(NamedTuple):
    """
    Container for committed group offset data.

    The Kafka offset commit API allows users to provide additional metadata
    (in the form of a string) when an offset is committed. This can be useful
    (for example) to store information about which node made the commit,
    what time the commit was made, etc.

    Keyword Arguments:
        offset (int): The offset to be committed
        metadata (str): Non-null metadata
        leader_epoch (int): The last known epoch from the leader / broker
    """
    offset: int | None = None
    metadata: str = ""
    leader_epoch: int = -1

class OffsetAndTimestamp(NamedTuple):
    """
    An offset and timestamp tuple

    Keyword Arguments:
        offset (int): An offset
        timestamp (int): The timestamp associated to the offset
        leader_epoch (int): The last known epoch from the leader / broker
    """
    offset: int
    timestamp: int
    leader_epoch: int

class MemberState:
    UNJOINED: Final = "<unjoined>"
    REBALANCING: Final = "<rebalancing>"
    STABLE: Final = "<stable>"

class ConsumerGroupMetadata(NamedTuple):
    """
    A snapshot of a consumer's group membership.

    The first four fields are the KIP-447 fencing identity: pass the snapshot to
    KafkaProducer.send_offsets_to_transaction() so the broker can fence stale
    consumer instances when committing offsets inside a transaction. The broker
    uses member_id + generation_id + group_instance_id to verify the producer is
    acting on behalf of the current group generation.

    The ``state`` field exposes the live MemberState (it is ignored by the
    producer/fencing path). It lets callers observe whether the consumer has
    converged on a stable assignment - useful for monitoring and for tests that
    wait for a group to finish rebalancing.

    Keyword Arguments:
        group_id (str): The consumer group id, or None for manual assignment.
        generation_id (int): The current generation id (-1 if unjoined).
        member_id (str): The current member id ('' if unjoined).
        group_instance_id (str): The static membership instance id, or None.
        state (str): The current MemberState (one of MemberState.UNJOINED,
            MemberState.REBALANCING, MemberState.STABLE).
    """
    group_id: str | None = None
    generation_id: int = -1
    member_id: str = ""
    group_instance_id: str | None = None
    state: Literal["<unjoined>", "<rebalancing>", "<stable>"] = ...  # Please, keep in sync with MemberState
