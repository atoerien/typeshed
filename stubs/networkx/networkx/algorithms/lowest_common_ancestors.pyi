"""Algorithms for finding the lowest common ancestor of trees and DAGs."""

from _typeshed import Incomplete
from collections.abc import Generator

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import _Node
from networkx.utils.backends import _dispatchable

__all__ = ["all_pairs_lowest_common_ancestor", "tree_all_pairs_lowest_common_ancestor", "lowest_common_ancestor"]

@_dispatchable
def all_pairs_lowest_common_ancestor(G: DiGraph[_Node], pairs=None):
    """
    Return the lowest common ancestor of all pairs or the provided pairs

    Parameters
    ----------
    G : NetworkX directed graph

    pairs : iterable of pairs of nodes, optional (default: all pairs)
        The pairs of nodes of interest.
        If None, will find the LCA of all pairs of nodes.

    Yields
    ------
    ((node1, node2), lca) : 2-tuple
        Where lca is least common ancestor of node1 and node2.
        Note that for the default case, the order of the node pair is not considered,
        e.g. you will not get both ``(a, b)`` and ``(b, a)``

    Raises
    ------
    NetworkXPointlessConcept
        If `G` is null.
    NetworkXError
        If `G` is not a DAG.

    Examples
    --------
    >>> from pprint import pprint

    The default behavior is to yield the lowest common ancestor for all
    possible combinations of nodes in `G`, including self-pairings:

    >>> G = nx.DiGraph([(0, 1), (0, 3), (1, 2)])
    >>> pprint(dict(nx.all_pairs_lowest_common_ancestor(G)))
    {(0, 0): 0,
     (0, 1): 0,
     (0, 2): 0,
     (0, 3): 0,
     (1, 1): 1,
     (1, 2): 1,
     (1, 3): 0,
     (2, 2): 2,
     (3, 2): 0,
     (3, 3): 3}

    The pairs argument can be used to limit the output to only the
    specified node pairings:

    >>> dict(nx.all_pairs_lowest_common_ancestor(G, pairs=[(1, 2), (2, 3)]))
    {(1, 2): 1, (2, 3): 0}

    Notes
    -----
    Only defined on non-null directed acyclic graphs.

    See Also
    --------
    lowest_common_ancestor
    """
    ...
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
def tree_all_pairs_lowest_common_ancestor(G: DiGraph[_Node], root: _Node | None = None, pairs=None) -> Generator[Incomplete]: ...
