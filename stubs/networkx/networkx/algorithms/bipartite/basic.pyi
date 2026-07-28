"""
==========================
Bipartite Graph Algorithms
==========================
"""

from _typeshed import Incomplete
from collections.abc import Collection, Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["is_bipartite", "is_bipartite_node_set", "color", "sets", "density", "degrees"]

@_dispatchable
def color(G: Graph[_Node]) -> dict[Incomplete, Incomplete]:
    """
    Returns a two-coloring of the graph.

    Raises an exception if the graph is not bipartite.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    color : dictionary
        A dictionary keyed by node with a 1 or 0 as data for each node color.

    Raises
    ------
    NetworkXError
        If the graph is not two-colorable.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.path_graph(4)
    >>> c = bipartite.color(G)
    >>> print(c)
    {0: 1, 1: 0, 2: 1, 3: 0}

    You can use this to set a node attribute indicating the bipartite set:

    >>> nx.set_node_attributes(G, c, "bipartite")
    >>> print(G.nodes[0]["bipartite"])
    1
    >>> print(G.nodes[1]["bipartite"])
    0
    """
    ...
@_dispatchable
def is_bipartite(G: Graph[_Node]) -> bool:
    """
    Returns True if graph G is bipartite, False if not.

    Parameters
    ----------
    G : NetworkX graph

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.path_graph(4)
    >>> print(bipartite.is_bipartite(G))
    True

    See Also
    --------
    color, is_bipartite_node_set
    """
    ...
@_dispatchable
def is_bipartite_node_set(G: Graph[_Node], nodes: Iterable[Incomplete]) -> bool:
    """
    Returns True if nodes and G/nodes are a bipartition of G.

    Parameters
    ----------
    G : NetworkX graph

    nodes: list or container
      Check if nodes are a one of a bipartite set.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.path_graph(4)
    >>> X = set([1, 3])
    >>> bipartite.is_bipartite_node_set(G, X)
    True

    Notes
    -----
    An exception is raised if the input nodes are not distinct, because in this
    case some bipartite algorithms will yield incorrect results.
    For connected graphs the bipartite sets are unique.  This function handles
    disconnected graphs.
    """
    ...
@_dispatchable
def sets(G: Graph[_Node], top_nodes: Iterable[Incomplete] | None = None) -> tuple[set[Incomplete], set[Incomplete]]:
    """
    Returns bipartite node sets of graph G.

    Raises an exception if the graph is not bipartite or if the input
    graph is disconnected and thus more than one valid solution exists.
    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.

    Parameters
    ----------
    G : NetworkX graph

    top_nodes : container, optional
      Container with all nodes in one bipartite node set. If not supplied
      it will be computed. But if more than one solution exists an exception
      will be raised.

    Returns
    -------
    X : set
      Nodes from one side of the bipartite graph.
    Y : set
      Nodes from the other side.

    Raises
    ------
    AmbiguousSolution
      Raised if the input bipartite graph is disconnected and no container
      with all nodes in one bipartite set is provided. When determining
      the nodes in each bipartite set more than one valid solution is
      possible if the input graph is disconnected.
    NetworkXError
      Raised if the input graph is not bipartite.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.path_graph(4)
    >>> X, Y = bipartite.sets(G)
    >>> list(X)
    [0, 2]
    >>> list(Y)
    [1, 3]

    See Also
    --------
    color
    """
    ...
@_dispatchable
def density(B: Graph[_Node], nodes: Collection[Incomplete]) -> float: ...
@_dispatchable
def degrees(B: Graph[_Node], nodes: Iterable[Incomplete], weight: str | None = None) -> tuple[Incomplete, Incomplete]: ...
