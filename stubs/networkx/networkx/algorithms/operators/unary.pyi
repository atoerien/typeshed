from _typeshed import Incomplete
from collections.abc import Hashable
from typing import TypeVar

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

_G = TypeVar("_G", bound=Graph[Hashable])

__all__ = ["complement", "reverse"]

@_dispatchable
def complement(G: Graph[_Node]) -> Graph[Incomplete]: ...
@_dispatchable
def reverse(G: _G, copy: bool = True) -> _G:
    """
    Returns the reverse directed graph of G.

    Parameters
    ----------
    G : directed graph
        A NetworkX directed graph
    copy : bool
        If True, then a new graph is returned. If False, then the graph is
        reversed in place.

    Returns
    -------
    H : directed graph
        The reversed G.

    Raises
    ------
    NetworkXError
        If graph is undirected.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5)])
    >>> G_reversed = nx.reverse(G)
    >>> G_reversed.edges()
    OutEdgeView([(2, 1), (3, 1), (3, 2), (4, 3), (5, 3)])
    """
    ...
