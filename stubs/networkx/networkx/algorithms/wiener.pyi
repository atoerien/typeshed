"""
Functions related to the Wiener Index of a graph.

The Wiener Index is a topological measure of a graph
related to the distance between nodes and their degree.
The Schultz Index and Gutman Index are similar measures.
They are used categorize molecules via the network of
atoms connected by chemical bonds. The indices are
correlated with functional aspects of the molecules.

References
----------
.. [1] `Wikipedia: Wiener Index <https://en.wikipedia.org/wiki/Wiener_index>`_
.. [2] M.V. Diudeaa and I. Gutman, Wiener-Type Topological Indices,
       Croatica Chemica Acta, 71 (1998), 21-51.
       https://hrcak.srce.hr/132323
"""

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["wiener_index", "schultz_index", "gutman_index", "hyper_wiener_index"]

@_dispatchable
def wiener_index(G: Graph[_Node], weight: str | None = None) -> float:
    """
    Returns the Wiener index of the given graph.

    The *Wiener index* of a graph is the sum of the shortest-path
    (weighted) distances between each pair of reachable nodes.
    For pairs of nodes in undirected graphs, only one orientation
    of the pair is counted.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or None, optional (default: None)
        If None, every edge has weight 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        The edge weights are used to computing shortest-path distances.

    Returns
    -------
    number
        The Wiener index of the graph `G`.

    Raises
    ------
    NetworkXError
        If the graph `G` is not connected.

    Notes
    -----
    If a pair of nodes is not reachable, the distance is assumed to be
    infinity. This means that for graphs that are not
    strongly-connected, this function returns ``inf``.

    The Wiener index is not usually defined for directed graphs, however
    this function uses the natural generalization of the Wiener index to
    directed graphs.

    Examples
    --------
    The Wiener index of the (unweighted) complete graph on *n* nodes
    equals the number of pairs of the *n* nodes, since each pair of
    nodes is at distance one::

        >>> n = 10
        >>> G = nx.complete_graph(n)
        >>> nx.wiener_index(G) == n * (n - 1) / 2
        True

    Graphs that are not strongly-connected have infinite Wiener index::

        >>> G = nx.empty_graph(2)
        >>> nx.wiener_index(G)
        inf

    References
    ----------
    .. [1] `Wikipedia: Wiener Index <https://en.wikipedia.org/wiki/Wiener_index>`_
    """
    ...
@_dispatchable
def schultz_index(G: Graph[_Node], weight: str | None = None) -> float: ...
@_dispatchable
def gutman_index(G: Graph[_Node], weight: str | None = None) -> float: ...
@_dispatchable
def hyper_wiener_index(G: Graph[_Node], weight: str | None = None) -> float: ...
