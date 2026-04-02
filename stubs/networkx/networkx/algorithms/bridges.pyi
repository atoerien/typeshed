"""Bridge-finding algorithms."""

from collections.abc import Generator
from typing import overload

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["bridges", "has_bridges", "local_bridges"]

@_dispatchable
def bridges(G: Graph[_Node], root: _Node | None = None) -> Generator[_Node]: ...
@_dispatchable
def has_bridges(G: Graph[_Node], root: _Node | None = None) -> bool:
    """
    Decide whether a graph has any bridges.

    A *bridge* in a graph is an edge whose removal causes the number of
    connected components of the graph to increase.

    Parameters
    ----------
    G : undirected graph

    root : node (optional)
       A node in the graph `G`. If specified, only the bridges in the
       connected component containing this node will be considered.

    Returns
    -------
    bool
       Whether the graph (or the connected component containing `root`)
       has any bridges.

    Raises
    ------
    NodeNotFound
       If `root` is not in the graph `G`.

    NetworkXNotImplemented
        If `G` is a directed graph.

    Examples
    --------
    The barbell graph with parameter zero has a single bridge::

        >>> G = nx.barbell_graph(10, 0)
        >>> nx.has_bridges(G)
        True

    On the other hand, the cycle graph has no bridges::

        >>> G = nx.cycle_graph(5)
        >>> nx.has_bridges(G)
        False

    Notes
    -----
    This implementation uses the :func:`networkx.bridges` function, so
    it shares its worst-case time complexity, $O(m + n)$, ignoring
    polylogarithmic factors, where $n$ is the number of nodes in the
    graph and $m$ is the number of edges.
    """
    ...
@overload
def local_bridges(G: Graph[_Node], with_span: bool = True, weight: str | None = None) -> Generator[tuple[_Node, _Node]]: ...
@overload
def local_bridges(G: Graph[_Node], with_span: bool = True, weight: str | None = None) -> Generator[tuple[_Node, _Node, int]]: ...
