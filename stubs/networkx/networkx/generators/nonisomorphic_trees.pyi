"""
Implementation of the Wright, Richmond, Odlyzko and McKay (WROM)
algorithm for the enumeration of all non-isomorphic free trees of a
given order.  Rooted trees are represented by level sequences, i.e.,
lists in which the i-th element specifies the distance of vertex i to
the root.
"""

from _typeshed import Incomplete
from collections.abc import Generator

from networkx.utils.backends import _dispatchable

__all__ = ["nonisomorphic_trees", "number_of_nonisomorphic_trees"]

@_dispatchable
def nonisomorphic_trees(order: int) -> Generator[list[Incomplete]]: ...
@_dispatchable
def number_of_nonisomorphic_trees(order: int) -> int: ...
