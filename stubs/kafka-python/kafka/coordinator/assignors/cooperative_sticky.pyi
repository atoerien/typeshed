"""
KIP-429 cooperative sticky partition assignor.

Wraps :class:`StickyPartitionAssignor` (KIP-54) with the two-phase
"incremental cooperative" rebalancing protocol:

  * Members keep their assignment across JoinGroup - no global revoke.
  * The leader runs the sticky algorithm to compute the *ideal* final
    assignment, then identifies any partition that is moving from one
    owner to another and *removes it from the new owner's first-round
    assignment*. The current owner sees its assignment shrink, revokes
    the lost partition, and the broker is signaled (via
    ``request_rejoin``) that another rebalance is needed.
  * Round two: the freshly-revoked partition is owned by nobody; the
    sticky algorithm now gives it to its intended new owner.

This avoids the "stop the world" pause that EAGER mode imposes - each
member only pauses while it's processing the specific partitions
moving in or out of its own assignment.

References:
  * KIP-429: https://cwiki.apache.org/confluence/x/vAclBg
  * Java: org.apache.kafka.clients.consumer.CooperativeStickyAssignor
"""

from _typeshed import Incomplete

from kafka.coordinator.assignors.abstract import RebalanceProtocol
from kafka.coordinator.assignors.sticky.sticky_assignor import StickyAssignorMemberMetadataV1, StickyPartitionAssignor
from kafka.protocol.consumer.metadata import ConsumerProtocolAssignment, ConsumerProtocolSubscription

class CooperativeStickyAssignor(StickyPartitionAssignor):
    """
    KIP-429 cooperative variant of the sticky assignor.

    Behaviorally identical to :class:`StickyPartitionAssignor` for
    final partition placement (it inherits the same algorithm) - the
    only difference is that movements are staged across two rebalance
    rounds so no member ever sees a partition assigned to it while
    another member still owns it.
    """
    name: str
    version: int
    def supported_protocols(self) -> list[RebalanceProtocol]: ...
    def metadata(self, topics) -> ConsumerProtocolSubscription: ...
    @classmethod
    def parse_member_metadata(cls, metadata) -> StickyAssignorMemberMetadataV1:
        """
        Decode a member's ``ConsumerProtocolSubscription``.

        Cooperative members carry owned partitions in the
        ``owned_partitions`` schema field (v1+) rather than the
        ``user_data`` blob the legacy sticky assignor uses. Returns
        the same ``StickyAssignorMemberMetadataV1`` shape so the
        underlying sticky algorithm can consume it unchanged.
        """
        ...
    def assign(self, cluster, members) -> dict[Incomplete, ConsumerProtocolAssignment]:
        """
        Cooperative two-phase assignment.

        1. Compute the ideal final sticky assignment.
        2. Build a map of currently-owned partitions across all
           members from their ``OwnedPartitions``.
        3. For any partition whose final owner differs from its
           current owner, remove it from the new owner's first-round
           assignment. The current owner sees its assignment shrink,
           revokes the partition, and re-joins; on round two the
           partition is unowned and the algorithm assigns it.
        """
        ...
