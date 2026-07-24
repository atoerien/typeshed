"""Set based operations for IP addresses and subnets."""

from collections.abc import Iterable, Iterator
from typing import TypeAlias
from typing_extensions import Never, Self

from netaddr.ip import IPAddress, IPNetwork, IPRange, _IPNetworkAddr

_IPIterable: TypeAlias = IPNetwork | IPRange | IPSet | Iterable[_IPNetworkAddr | IPRange | int]

class IPSet:
    """
    Represents an unordered collection (set) of unique IP addresses and
    subnets.
    """
    __slots__ = ("_cidrs", "__weakref__")
    def __init__(self, iterable: _IPIterable | None = None, flags: int = 0) -> None: ...
    def compact(self) -> None: ...
    def __hash__(self) -> Never: ...
    def __contains__(self, ip: _IPNetworkAddr) -> bool: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[IPAddress]: ...
    def iter_cidrs(self) -> list[IPNetwork]: ...
    def add(self, addr: IPRange | _IPNetworkAddr | int, flags: int = 0) -> None: ...
    def remove(self, addr: IPRange | _IPNetworkAddr | int, flags: int = 0) -> None: ...
    def pop(self) -> IPNetwork: ...
    def isdisjoint(self, other: IPSet) -> bool: ...
    def copy(self) -> Self: ...
    def update(self, iterable: _IPIterable, flags: int = 0) -> None: ...
    def clear(self) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: IPSet) -> bool: ...
    def issubset(self, other: IPSet) -> bool: ...
    __le__ = issubset
    def __gt__(self, other: IPSet) -> bool:
        """
        :param other: an IP set.

        :return: ``True`` if this IP set is greater than the ``other`` IP set,
            ``False`` otherwise.
        """
        ...
    def issuperset(self, other: IPSet) -> bool:
        """
        :param other: an IP set.

        :return: ``True`` if every IP address and subnet in other IP set
            is found within this one.
        """
        ...
    __ge__ = issuperset
    def union(self, other: IPSet) -> Self:
        """
        :param other: an IP set.

        :return: the union of this IP set and another as a new IP set
            (combines IP addresses and subnets from both sets).
        """
        ...
    __or__ = union
    def intersection(self, other: IPSet) -> IPSet:
        """
        :param other: an IP set.

        :return: the intersection of this IP set and another as a new IP set.
            (IP addresses and subnets common to both sets).
        """
        ...
    __and__ = intersection
    def symmetric_difference(self, other: IPSet) -> IPSet:
        """
        :param other: an IP set.

        :return: the symmetric difference of this IP set and another as a new
            IP set (all IP addresses and subnets that are in exactly one
            of the sets).
        """
        ...
    __xor__ = symmetric_difference
    def difference(self, other: IPSet) -> IPSet:
        """
        :param other: an IP set.

        :return: the difference between this IP set and another as a new IP
            set (all IP addresses and subnets that are in this IP set but
            not found in the other.)
        """
        ...
    __sub__ = difference
    def __len__(self) -> int:
        """:return: the cardinality of this IP set (i.e. sum of individual IP             addresses). Raises ``IndexError`` if size > maxsize (a Python             limitation). Use the .size property for subnets of any size."""
        ...
    @property
    def size(self) -> int:
        """
        The cardinality of this IP set (based on the number of individual IP
        addresses including those implicitly defined in subnets).
        """
        ...
    def iscontiguous(self) -> bool:
        """
        Returns True if the members of the set form a contiguous IP
        address range (with no gaps), False otherwise.

        :return: ``True`` if the ``IPSet`` object is contiguous.
        """
        ...
    def iprange(self) -> IPRange | None:
        """
        Generates an IPRange for this IPSet, if all its members
        form a single contiguous sequence.

        Raises ``ValueError`` if the set is not contiguous.

        :return: An ``IPRange`` for all IPs in the IPSet.
        """
        ...
    def iter_ipranges(self) -> Iterator[IPRange]:
        """
        Generate the merged IPRanges for this IPSet.

        In contrast to self.iprange(), this will work even when the IPSet is
        not contiguous. Adjacent IPRanges will be merged together, so you
        get the minimal number of IPRanges.
        """
        ...
