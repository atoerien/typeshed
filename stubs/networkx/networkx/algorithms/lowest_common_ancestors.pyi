"""Algorithms for finding the lowest common ancestor of trees and DAGs."""

from _typeshed import Incomplete
from collections.abc import Generator, Iterable, Iterator

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import _Node
from networkx.utils.backends import _dispatchable

__all__ = ["all_pairs_lowest_common_ancestor", "tree_all_pairs_lowest_common_ancestor", "lowest_common_ancestor"]

@_dispatchable
def all_pairs_lowest_common_ancestor(G: DiGraph[_Node], pairs: Iterable[Incomplete] | None = None): ...
@_dispatchable
def lowest_common_ancestor(G: DiGraph[_Node], node1, node2, default=None):
    """
    Compute the lowest common ancestor of the given pair of nodes.

    Parameters
    ----------
    G : NetworkX directed graph

    node1, node2 : nodes in the graph.

    default : object
        Returned if no common ancestor between `node1` and `node2`

    Returns
    -------
    The lowest common ancestor of node1 and node2,
    or default if they have no common ancestors.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> nx.add_path(G, (0, 1, 2, 3))
    >>> nx.add_path(G, (0, 4, 3))
    >>> nx.lowest_common_ancestor(G, 2, 4)
    0

    See Also
    --------
    all_pairs_lowest_common_ancestor
    """
    ...
@_dispatchable
def tree_all_pairs_lowest_common_ancestor(
    G: DiGraph[_Node], root: _Node | None = None, pairs: Iterator[Incomplete] | None = None
) -> Generator[Incomplete]: ...
