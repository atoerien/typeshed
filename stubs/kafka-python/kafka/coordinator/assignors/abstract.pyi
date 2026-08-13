import abc
from enum import IntEnum

class RebalanceProtocol(IntEnum):
    EAGER = 0
    COOPERATIVE = 1

class AbstractPartitionAssignor(metaclass=abc.ABCMeta):
    """
    Abstract assignor implementation which does some common grunt work (in particular collecting
    partition counts which are always needed in assignors).
    """
    @property
    @abc.abstractmethod
    def name(self): ...
    def supported_protocols(self) -> list[RebalanceProtocol]: ...
    @abc.abstractmethod
    def assign(self, cluster, members):
        """
        Perform group assignment given cluster metadata and member subscriptions

        Arguments:
            cluster (ClusterMetadata): metadata for use in assignment
            members (dict of {member_id: Subscription}): decoded metadata
                for each member in the group, including group_instance_id
                when available.

        Returns:
            dict: {member_id: MemberAssignment}
        """
        ...
    @abc.abstractmethod
    def metadata(self, topics):
        """
        Generate ProtocolMetadata to be submitted via JoinGroupRequest.

        Arguments:
            topics (set): a member's subscribed topics

        Returns:
            MemberMetadata struct
        """
        ...
    @abc.abstractmethod
    def on_assignment(self, assignment, generation): ...
