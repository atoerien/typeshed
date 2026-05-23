"""Other useful structs """

from _typeshed import Incomplete
from typing import NamedTuple

class TopicPartition(NamedTuple):
    """TopicPartition(topic, partition)"""
    topic: str
    partition: int

class BrokerMetadata(NamedTuple):
    """BrokerMetadata(nodeId, host, port, rack)"""
    nodeId: int
    host: str
    port: int
    rack: str | None

class PartitionMetadata(NamedTuple):
    """PartitionMetadata(topic, partition, leader, leader_epoch, replicas, isr, offline_replicas, error)"""
    topic: str
    partition: int
    leader: int
    leader_epoch: int | None
    replicas: list[int]
    isr: list[int]
    offline_replicas: list[int]
    error: Incomplete

class OffsetAndMetadata(NamedTuple):
    """OffsetAndMetadata(offset, metadata, leader_epoch)"""
    offset: int
    metadata: str
    leader_epoch: int

class OffsetAndTimestamp(NamedTuple):
    """OffsetAndTimestamp(offset, timestamp, leader_epoch)"""
    offset: int
    timestamp: int
    leader_epoch: int

class MemberInformation(NamedTuple):
    """MemberInformation(member_id, client_id, client_host, member_metadata, member_assignment)"""
    member_id: str
    client_id: str
    client_host: str
    member_metadata: Incomplete
    member_assignment: Incomplete

class GroupInformation(NamedTuple):
    """GroupInformation(error_code, group, state, protocol_type, protocol, members, authorized_operations)"""
    error_code: int
    group: str
    state: str
    protocol_type: str
    protocol: str
    members: list[MemberInformation]
    authorized_operations: list[str]

class RetryOptions(NamedTuple):
    """RetryOptions(limit, backoff_ms, retry_on_timeouts)"""
    limit: int
    backoff_ms: int
    retry_on_timeouts: bool
