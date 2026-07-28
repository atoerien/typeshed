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
def nonisomorphic_trees(order: int) -> Generator[list[Incomplete]]:
    """
    Generate nonisomorphic trees of specified `order`.

    Parameters
    ----------
    order : int
       order of the desired tree(s)

    Yields
    ------
    `networkx.Graph` instances
       A tree with `order` number of nodes that is not isomorphic to any other
       yielded tree.

    Raises
    ------
    ValueError
       If `order` is negative.

    Examples
    --------
    There are 11 unique (non-isomorphic) trees with 7 nodes.

    >>> n = 7
    >>> nit_list = list(nx.nonisomorphic_trees(n))
    >>> len(nit_list) == nx.number_of_nonisomorphic_trees(n) == 11
    True

    All trees yielded by the generator have the specified order.

    >>> all(len(G) == n for G in nx.nonisomorphic_trees(n))
    True

    Each tree is nonisomorphic to every other tree yielded by the generator.
    >>> seen = []
    >>> for G in nx.nonisomorphic_trees(n):
    ...     assert not any(nx.is_isomorphic(G, H) for H in seen)
    ...     seen.append(G)

    See Also
    --------
    number_of_nonisomorphic_trees
    """
    ...
@_dispatchable
def number_of_nonisomorphic_trees(order: int) -> int:
    """
    Returns the number of nonisomorphic trees of the specified `order`.

    Based on an algorithm by Alois P. Heinz in
    `OEIS entry A000055 <https://oeis.org/A000055>`_. Complexity is ``O(n ** 3)``.

    Parameters
    ----------
    order : int
       Order of the desired tree(s).

    Returns
    -------
    int
       Number of nonisomorphic trees with `order` number of nodes.

    Raises
    ------
    ValueError
       If `order` is negative.

    Examples
    --------
    >>> nx.number_of_nonisomorphic_trees(10)
    106

    See Also
    --------
    nonisomorphic_trees
    """
    ...
