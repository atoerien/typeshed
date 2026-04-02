"""Eulerian circuits and graphs."""

from _typeshed import Incomplete
from collections.abc import Generator

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["is_eulerian", "eulerian_circuit", "eulerize", "is_semieulerian", "has_eulerian_path", "eulerian_path"]

@_dispatchable
def is_eulerian(G: Graph[_Node]) -> bool:
    """
    Returns True if and only if `G` is Eulerian.

    A graph is *Eulerian* if it has an Eulerian circuit. An *Eulerian
    circuit* is a closed walk that includes each edge of a graph exactly
    once.

    Graphs with isolated vertices (i.e. vertices with zero degree) are not
    considered to have Eulerian circuits. Therefore, if the graph is not
    connected (or not strongly connected, for directed graphs), this function
    returns False.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    Examples
    --------
    >>> nx.is_eulerian(nx.DiGraph({0: [3], 1: [2], 2: [3], 3: [0, 1]}))
    True
    >>> nx.is_eulerian(nx.complete_graph(5))
    True
    >>> nx.is_eulerian(nx.petersen_graph())
    False

    If you prefer to allow graphs with isolated vertices to have Eulerian circuits,
    you can first remove such vertices and then call `is_eulerian` as below example shows.

    >>> G = nx.Graph([(0, 1), (1, 2), (0, 2)])
    >>> G.add_node(3)
    >>> nx.is_eulerian(G)
    False

    >>> G.remove_nodes_from(list(nx.isolates(G)))
    >>> nx.is_eulerian(G)
    True
    """
    ...
@_dispatchable
def is_semieulerian(G: Graph[_Node]) -> bool:
    """
    Return True iff `G` is semi-Eulerian.

    G is semi-Eulerian if it has an Eulerian path but no Eulerian circuit.

    See Also
    --------
    has_eulerian_path
    is_eulerian
    """
    ...
@_dispatchable
def eulerian_circuit(G: Graph[_Node], source: _Node | None = None, keys: bool = False) -> Generator[Incomplete, Incomplete]: ...
@_dispatchable
def has_eulerian_path(G: Graph[_Node], source: _Node | None = None) -> bool:
    """
    Return True iff `G` has an Eulerian path.

    An Eulerian path is a path in a graph which uses each edge of a graph
    exactly once. If `source` is specified, then this function checks
    whether an Eulerian path that starts at node `source` exists.

    A directed graph has an Eulerian path iff:
        - at most one vertex has out_degree - in_degree = 1,
        - at most one vertex has in_degree - out_degree = 1,
        - every other vertex has equal in_degree and out_degree,
        - and all of its vertices belong to a single connected
          component of the underlying undirected graph.

    If `source` is not None, an Eulerian path starting at `source` exists if no
    other node has out_degree - in_degree = 1. This is equivalent to either
    there exists an Eulerian circuit or `source` has out_degree - in_degree = 1
    and the conditions above hold.

    An undirected graph has an Eulerian path iff:
        - exactly zero or two vertices have odd degree,
        - and all of its vertices belong to a single connected component.

    If `source` is not None, an Eulerian path starting at `source` exists if
    either there exists an Eulerian circuit or `source` has an odd degree and the
    conditions above hold.

    Graphs with isolated vertices (i.e. vertices with zero degree) are not considered
    to have an Eulerian path. Therefore, if the graph is not connected (or not strongly
    connected, for directed graphs), this function returns False.

    Parameters
    ----------
    G : NetworkX Graph
        The graph to find an euler path in.

    source : node, optional
        Starting node for path.

    Returns
    -------
    Bool : True if G has an Eulerian path.

    Examples
    --------
    If you prefer to allow graphs with isolated vertices to have Eulerian path,
    you can first remove such vertices and then call `has_eulerian_path` as below example shows.

    >>> G = nx.Graph([(0, 1), (1, 2), (0, 2)])
    >>> G.add_node(3)
    >>> nx.has_eulerian_path(G)
    False

    >>> G.remove_nodes_from(list(nx.isolates(G)))
    >>> nx.has_eulerian_path(G)
    True

    See Also
    --------
    is_eulerian
    eulerian_path
    """
    ...
@_dispatchable
def eulerian_path(G: Graph[_Node], source=None, keys: bool = False) -> Generator[Incomplete, Incomplete]: ...
@_dispatchable
def eulerize(G: Graph[_Node]):
    """
    Transforms a graph into an Eulerian graph.

    If `G` is Eulerian the result is `G` as a MultiGraph, otherwise the result is a smallest
    (in terms of the number of edges) multigraph whose underlying simple graph is `G`.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph

    Returns
    -------
    G : NetworkX multigraph

    Raises
    ------
    NetworkXError
       If the graph is not connected.

    See Also
    --------
    is_eulerian
    eulerian_circuit

    References
    ----------
    .. [1] J. Edmonds, E. L. Johnson.
       Matching, Euler tours and the Chinese postman.
       Mathematical programming, Volume 5, Issue 1 (1973), 111-114.
    .. [2] https://en.wikipedia.org/wiki/Eulerian_path
    .. [3] http://web.math.princeton.edu/math_alive/5/Notes1.pdf

    Examples
    --------
        >>> G = nx.complete_graph(10)
        >>> H = nx.eulerize(G)
        >>> nx.is_eulerian(H)
        True
    """
    ...
