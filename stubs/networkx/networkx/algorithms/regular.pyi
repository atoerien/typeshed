from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["is_regular", "is_k_regular", "k_factor"]

@_dispatchable
def is_regular(G: Graph[_Node]) -> bool:
    """
    Determines whether a graph is regular.

    A regular graph is a graph where all nodes have the same degree. A regular
    digraph is a graph where all nodes have the same indegree and all nodes
    have the same outdegree.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        Whether the given graph or digraph is regular.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 4), (4, 1)])
    >>> nx.is_regular(G)
    True
    """
    ...
@_dispatchable
def is_k_regular(G: Graph[_Node], k) -> bool:
    """
    Determines whether the graph ``G`` is a k-regular graph.

    A k-regular graph is a graph where each vertex has degree k.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        Whether the given graph is k-regular.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
    >>> nx.is_k_regular(G, k=3)
    False
    """
    ...
@_dispatchable
def k_factor(G: Graph[_Node], k: int, matching_weight: str | None = "weight") -> Graph[Incomplete]: ...
