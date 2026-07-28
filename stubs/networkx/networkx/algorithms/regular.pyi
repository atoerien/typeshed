"""Functions for computing and verifying regular graphs."""

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
def k_factor(G: Graph[_Node], k: int, matching_weight: str | None = "weight") -> Graph[Incomplete]:
    """
    Compute a `k`-factor of a graph.

    A `k`-factor of a graph is a spanning `k`-regular subgraph.
    A spanning `k`-regular subgraph of `G` is a subgraph that contains
    each node of `G` and a subset of the edges of `G` such that each
    node has degree `k`.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    k : int
        The degree of the `k`-factor.

    matching_weight: string, optional (default="weight")
        Edge attribute name corresponding to the edge weight.
        If not present, the edge is assumed to have weight 1.
        Used for finding the max-weighted perfect matching.

    Returns
    -------
    NetworkX graph
        A `k`-factor of `G`.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
    >>> KF = nx.k_factor(G, k=1)
    >>> KF.edges()
    EdgeView([(1, 2), (3, 4)])

    References
    ----------
    .. [1] "An algorithm for computing simple k-factors.",
       Meijer, Henk, Yurai Núñez-Rodríguez, and David Rappaport,
       Information processing letters, 2009.
    """
    ...
