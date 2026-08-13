"""Group management mixin for KafkaAdminClient."""

import sys
from _typeshed import Incomplete

from kafka.util import EnumHelper

class GroupAdminMixin:
    """Mixin providing consumer group management methods for KafkaAdminClient."""
    config: dict[Incomplete, Incomplete]
    def describe_groups(
        self, group_ids, group_coordinator_id: int | None = None, include_authorized_operations: bool = False
    ):
        """
        Describe a set of consumer groups.

        Any errors are immediately raised.

        Arguments:
            group_ids: A list of consumer group IDs. These are typically the
                group names as strings.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the groups' coordinator
                broker. If set to None, it will query the cluster for each group to
                find that group's coordinator. Explicitly specifying this can be
                useful for avoiding extra network round trips if you already know
                the group coordinator. This is only useful when all the group_ids
                have the same coordinator, otherwise it will error. Default: None.

        Returns:
            A dict of {group_id: {key: val}}. key/vals are simple to_dict translations
                of the raw results from DescribeGroupsResponse (with inline decoding
                of ConsumerSubscription and ConsumerAssignment metadata, and conversion
                of acl set ints to semantic enums).
        """
        ...
    def list_groups(self, broker_ids=None, states_filter=None, types_filter=None):
        """
        List all consumer groups known to the cluster.

        This returns a list of Group dicts. The tuples are
        composed of the consumer group name and the consumer group protocol
        type.

        Only consumer groups that store their offsets in Kafka are returned.
        The protocol type will be an empty string for groups created using
        Kafka < 0.9 APIs because, although they store their offsets in Kafka,
        they don't use Kafka for group coordination. For groups created using
        Kafka >= 0.9, the protocol type will typically be "consumer".

        As soon as any error is encountered, it is immediately raised.

        Keyword Arguments:
            broker_ids ([int], optional): A list of broker node_ids to query for consumer
                groups. If set to None, will query all brokers in the cluster.
                Explicitly specifying broker(s) can be useful for determining which
                consumer groups are coordinated by those broker(s). Default: None
            states_filter (list, optional): Filter groups by state. Values
                may be :class:`GroupState` members, their string names
                (case-insensitive, hyphen or underscore), or raw protocol
                strings (e.g. ``['Stable', 'Empty']``). Requires broker
                >= 3.0 (KIP-518). Default: None (no filter).
            types_filter (list, optional): Filter groups by type. Values
                may be :class:`GroupType` members, their string names
                (case-insensitive), or raw protocol strings (e.g.
                ``['consumer', 'classic', 'share']``). Requires broker
                >= 4.0 (KIP-848). Default: None (no filter).

        Returns:
            List of group data dicts, with key/vals from ListGroupsRequest
        """
        ...
    def list_group_offsets(self, group_specs):
        """
        Fetch committed offsets for one or more consumer groups.

        On brokers supporting OffsetFetch v8+ (Apache Kafka 3.0+, KIP-709), this
        issues a single OffsetFetch per coordinator covering all groups
        hosted by that coordinator. On older brokers it currently only supports
        one consumer group (per coordinator).

        Arguments:
            group_specs (dict): Mapping of group_id (str) to either a list of
                :class:`~kafka.TopicPartition` to fetch, or None to fetch all
                committed offsets for that group.
                Or, one or more group_id (str or list[str]) to fetch all offsets
                for each group.

        Returns:
            A dict mapping group_id (str) to a dict mapping
                :class:`~kafka.TopicPartition` to
                :class:`~kafka.structs.OffsetAndMetadata`.

        Raises:
            UnsupportedVersionError: if multiple groups are requested against
                a broker that does not support OffsetFetch v8+; or if group_spec
                with value None against a broker that does not support
                OffsetFetch v2+.
            BrokerResponseError: as soon as any group- or partition-level error
                is encountered.
        """
        ...
    def delete_groups(self, group_ids, group_coordinator_id: int | None = None):
        """
        Delete Group Offsets for given consumer groups.

        Note:
        This does not verify that the group ids actually exist and
        group_coordinator_id is the correct coordinator for all these groups.

        The result needs checking for potential errors.

        Arguments:
            group_ids ([str]): The consumer group ids of the groups which are to be deleted.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the broker which is
                the coordinator for all the groups. Default: None.

        Returns:
            A list of tuples (group_id, KafkaError)
        """
        ...
    def alter_group_offsets(self, group_id: str, offsets, group_coordinator_id: int | None = None):
        """
        Alter committed offsets for a consumer group.

        The group must have no active members (i.e. be empty or dead) for
        the commit to succeed; otherwise individual partitions may return
        ``UNKNOWN_MEMBER_ID`` or similar errors.

        Arguments:
            group_id (str): The consumer group id.
            offsets (dict): A dict mapping :class:`~kafka.TopicPartition` to
                :class:`~kafka.structs.OffsetAndMetadata`.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the group's
                coordinator broker. If None, the cluster will be queried to
                locate the coordinator. Default: None.

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to the
            partition-level :class:`~kafka.errors.KafkaError` class
            (``NoError`` on success).
        """
        ...
    def reset_group_offsets(self, group_id: str, offset_specs, group_coordinator_id: int | None = None):
        """
        Reset committed offsets for a consumer group.

        The group must have no active members (i.e. be empty or dead) for
        the reset to succeed; otherwise individual partitions may return
        ``UNKNOWN_MEMBER_ID`` or similar errors.

        Each dict value selects how the target offset is produced. All
        resulting offsets are clamped to the partition's
        ``[earliest, latest]`` range; values that resolve to
        ``UNKNOWN_OFFSET`` (e.g. a timestamp beyond the last record) are
        clamped to ``latest``.

        Arguments:
            group_id (str): The consumer group id.
            offset_specs (dict): A dict mapping :class:`~kafka.TopicPartition` to
                one of:

                * :class:`~kafka.admin.OffsetSpec` (e.g. ``OffsetSpec.EARLIEST``,
                  ``OffsetSpec.LATEST``, ``OffsetSpec.MAX_TIMESTAMP``):
                  resolved server-side via ListOffsets.
                * :class:`~kafka.admin.OffsetTimestamp` (ms since epoch):
                  resolved server-side to the earliest offset whose timestamp
                  is ``>=`` the given value.
                * Plain ``int``: an explicit committed offset (no server-side
                  resolution), which is still clamped to the valid range.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the group's
                coordinator broker. If None, the cluster will be queried to
                locate the coordinator. Default: None.

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to dict of
            {'error': :class:`~kafka.errors.KafkaError` class, 'offset': int}.
            The ``offset`` value is the post-clamp value that was committed.
        """
        ...
    def delete_group_offsets(self, group_id: str, partitions, group_coordinator_id: int | None = None):
        """
        Delete committed offsets for a consumer group.

        The group must have no active members subscribed to the given topics;
        otherwise partitions may fail with ``GROUP_SUBSCRIBED_TO_TOPIC``.

        Arguments:
            group_id (str): The consumer group id.
            partitions: An iterable of :class:`~kafka.TopicPartition` whose
                committed offsets should be deleted.

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the group's
                coordinator broker. If None, the cluster will be queried to
                locate the coordinator. Default: None.

        Returns:
            dict: A dict mapping :class:`~kafka.TopicPartition` to the
            partition-level :class:`~kafka.errors.KafkaError` class
            (``NoError`` on success).

        Raises:
            KafkaError: If the response contains a top-level error (e.g.
                ``GroupIdNotFoundError``, ``NonEmptyGroupError``).
        """
        ...
    def remove_group_members(self, group_id: str, members, group_coordinator_id: int | None = None):
        """
        Remove members from a consumer group.

        On brokers supporting LeaveGroup v3+ (Kafka 2.3+), a single batched
        request is sent. On older brokers, falls back to one single-member
        LeaveGroupRequest per member (in which case ``group_instance_id`` is
        not supported and ``member_id`` is required).

        Arguments:
            group_id (str): The consumer group id.
            members: An iterable of :class:`~kafka.admin.MemberToRemove`.
                Each entry must set at least one of ``member_id`` or,
                if brokers support LeaveGroup v3+, ``group_instance_id``.
                ``reason`` is only sent to brokers supporting
                LeaveGroup v5+ (KIP-800).

        Keyword Arguments:
            group_coordinator_id (int, optional): The node_id of the group's
                coordinator broker. If None, the cluster will be queried to
                locate the coordinator. Default: None.

        Returns:
            dict: A dict mapping :class:`~kafka.admin.MemberToRemove` to the
            per-member :class:`~kafka.errors.KafkaError` class
            (``NoError`` on success). The key's ``reason`` is always None in
            the result (not echoed by the broker).

        Raises:
            KafkaError: If a batched response contains a top-level error.
            UnsupportedVersionError: If the broker does not support batched
                LeaveGroupRequest and any member uses ``group_instance_id``.
        """
        ...

class MemberToRemove:
    """
    A consumer group member to remove via Admin.remove_group_members

    At least one of ``member_id`` (identifying a dynamic group member)
    or ``group_instance_id`` (identifying a static group member) must be set.

    Keyword Arguments:
        member_id (str or None): The dynamic member id (as assigned by the
            coordinator in JoinGroupResponse). Use None for static-only removal.
        group_instance_id (str or None): The static member instance id (the
            ``group.instance.id`` configured on the member). Requires LeaveGroup
            v3+ (Kafka 2.3+).
        reason (str or None): Optional reason for removal (propagated to the
            broker on LeaveGroup v5+; ignored on older brokers).
    """
    __slots__ = ("member_id", "group_instance_id", "reason")
    member_id: str | None
    group_instance_id: str | None
    reason: str | None
    def __init__(self, member_id: str | None = None, group_instance_id: str | None = None, reason: str | None = None) -> None: ...
    def __eq__(self, other: MemberToRemove) -> bool: ...  # type: ignore[override]
    def __hash__(self) -> int: ...

if sys.version_info >= (3, 11):
    from enum import StrEnum

    class GroupState(EnumHelper, StrEnum):
        """Consumer group states as reported by the broker (KIP-518, KIP-848)."""
        UNKNOWN = "Unknown"
        PREPARING_REBALANCE = "PreparingRebalance"
        COMPLETING_REBALANCE = "CompletingRebalance"
        STABLE = "Stable"
        DEAD = "Dead"
        EMPTY = "Empty"
        ASSIGNING = "Assigning"
        RECONCILING = "Reconciling"

    class GroupType(EnumHelper, StrEnum):
        """Consumer group protocol types (KIP-848)."""
        UNKNOWN = "Unknown"
        CLASSIC = "classic"
        CONSUMER = "consumer"
        SHARE = "share"

else:
    from enum import Enum

    class GroupState(EnumHelper, str, Enum):
        """Consumer group states as reported by the broker (KIP-518, KIP-848)."""
        UNKNOWN = "Unknown"
        PREPARING_REBALANCE = "PreparingRebalance"
        COMPLETING_REBALANCE = "CompletingRebalance"
        STABLE = "Stable"
        DEAD = "Dead"
        EMPTY = "Empty"
        ASSIGNING = "Assigning"
        RECONCILING = "Reconciling"

    class GroupType(EnumHelper, str, Enum):
        """Consumer group protocol types (KIP-848)."""
        UNKNOWN = "Unknown"
        CLASSIC = "classic"
        CONSUMER = "consumer"
        SHARE = "share"
