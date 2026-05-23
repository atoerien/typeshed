from _typeshed import Incomplete
from typing import NamedTuple

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor
from kafka.protocol.struct import Struct

log: Incomplete

class ConsumerGenerationPair(NamedTuple):
    """ConsumerGenerationPair(consumer, generation)"""
    consumer: Incomplete
    generation: Incomplete

def has_identical_list_elements(list_):
    """
    Checks if all lists in the collection have the same members

    Arguments:
      list_: collection of lists

    Returns:
      true if all lists in the collection have the same members; false otherwise
    """
    ...
def subscriptions_comparator_key(element): ...
def partitions_comparator_key(element): ...
def remove_if_present(collection, element) -> None: ...

class StickyAssignorMemberMetadataV1(NamedTuple):
    """StickyAssignorMemberMetadataV1(subscription, partitions, generation)"""
    subscription: Incomplete
    partitions: Incomplete
    generation: Incomplete

class StickyAssignorUserDataV1(Struct):
    """
    Used for preserving consumer's previously assigned partitions
    list and sending it as user data to the leader during a rebalance
    """
    SCHEMA: Incomplete

class StickyAssignmentExecutor:
    members: Incomplete
    current_assignment: Incomplete
    previous_assignment: Incomplete
    current_partition_consumer: Incomplete
    is_fresh_assignment: bool
    partition_to_all_potential_consumers: Incomplete
    consumer_to_all_potential_partitions: Incomplete
    sorted_current_subscriptions: Incomplete
    sorted_partitions: Incomplete
    unassigned_partitions: Incomplete
    revocation_required: bool
    partition_movements: Incomplete
    def __init__(self, cluster, members) -> None: ...
    def perform_initial_assignment(self) -> None: ...
    def balance(self) -> None: ...
    def get_final_assignment(self, member_id): ...

class StickyPartitionAssignor(AbstractPartitionAssignor):
    """
    https://cwiki.apache.org/confluence/display/KAFKA/KIP-54+-+Sticky+Partition+Assignment+Strategy

    The sticky assignor serves two purposes. First, it guarantees an assignment that is as balanced as possible, meaning either:
    - the numbers of topic partitions assigned to consumers differ by at most one; or
    - each consumer that has 2+ fewer topic partitions than some other consumer cannot get any of those topic partitions transferred to it.

    Second, it preserved as many existing assignment as possible when a reassignment occurs.
    This helps in saving some of the overhead processing when topic partitions move from one consumer to another.

    Starting fresh it would work by distributing the partitions over consumers as evenly as possible.
    Even though this may sound similar to how round robin assignor works, the second example below shows that it is not.
    During a reassignment it would perform the reassignment in such a way that in the new assignment
    - topic partitions are still distributed as evenly as possible, and
    - topic partitions stay with their previously assigned consumers as much as possible.

    The first goal above takes precedence over the second one.

    Example 1.
    Suppose there are three consumers C0, C1, C2,
    four topics t0, t1, t2, t3, and each topic has 2 partitions,
    resulting in partitions t0p0, t0p1, t1p0, t1p1, t2p0, t2p1, t3p0, t3p1.
    Each consumer is subscribed to all three topics.

    The assignment with both sticky and round robin assignors will be:
    - C0: [t0p0, t1p1, t3p0]
    - C1: [t0p1, t2p0, t3p1]
    - C2: [t1p0, t2p1]

    Now, let's assume C1 is removed and a reassignment is about to happen. The round robin assignor would produce:
    - C0: [t0p0, t1p0, t2p0, t3p0]
    - C2: [t0p1, t1p1, t2p1, t3p1]

    while the sticky assignor would result in:
    - C0 [t0p0, t1p1, t3p0, t2p0]
    - C2 [t1p0, t2p1, t0p1, t3p1]
    preserving all the previous assignments (unlike the round robin assignor).


    Example 2.
    There are three consumers C0, C1, C2,
    and three topics t0, t1, t2, with 1, 2, and 3 partitions respectively.
    Therefore, the partitions are t0p0, t1p0, t1p1, t2p0, t2p1, t2p2.
    C0 is subscribed to t0;
    C1 is subscribed to t0, t1;
    and C2 is subscribed to t0, t1, t2.

    The round robin assignor would come up with the following assignment:
    - C0 [t0p0]
    - C1 [t1p0]
    - C2 [t1p1, t2p0, t2p1, t2p2]

    which is not as balanced as the assignment suggested by sticky assignor:
    - C0 [t0p0]
    - C1 [t1p0, t1p1]
    - C2 [t2p0, t2p1, t2p2]

    Now, if consumer C0 is removed, these two assignors would produce the following assignments.
    Round Robin (preserves 3 partition assignments):
    - C1 [t0p0, t1p1]
    - C2 [t1p0, t2p0, t2p1, t2p2]

    Sticky (preserves 5 partition assignments):
    - C1 [t1p0, t1p1, t0p0]
    - C2 [t2p0, t2p1, t2p2]
    """
    DEFAULT_GENERATION_ID: int
    name: str
    version: int
    member_assignment: Incomplete
    generation = DEFAULT_GENERATION_ID
    @classmethod
    def assign(cls, cluster, members):
        """
        Performs group assignment given cluster metadata and member subscriptions

        Arguments:
            cluster (ClusterMetadata): cluster metadata
            members (dict of {member_id: MemberMetadata}): decoded metadata for each member in the group.

        Returns:
          dict: {member_id: MemberAssignment}
        """
        ...
    @classmethod
    def parse_member_metadata(cls, metadata):
        """
        Parses member metadata into a python object.
        This implementation only serializes and deserializes the StickyAssignorMemberMetadataV1 user data,
        since no StickyAssignor written in Python was deployed ever in the wild with version V0, meaning that
        there is no need to support backward compatibility with V0.

        Arguments:
          metadata (MemberMetadata): decoded metadata for a member of the group.

        Returns:
          parsed metadata (StickyAssignorMemberMetadataV1)
        """
        ...
    @classmethod
    def metadata(cls, topics): ...
    @classmethod
    def on_assignment(cls, assignment) -> None:
        """
        Callback that runs on each assignment. Updates assignor's state.

        Arguments:
          assignment: MemberAssignment
        """
        ...
    @classmethod
    def on_generation_assignment(cls, generation) -> None:
        """
        Callback that runs on each assignment. Updates assignor's generation id.

        Arguments:
          generation: generation id
        """
        ...
