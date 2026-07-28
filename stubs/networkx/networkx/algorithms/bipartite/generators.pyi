"""Generators and functions for bipartite graphs."""

from _typeshed import Incomplete
from collections.abc import Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = [
    "configuration_model",
    "havel_hakimi_graph",
    "reverse_havel_hakimi_graph",
    "alternating_havel_hakimi_graph",
    "preferential_attachment_graph",
    "random_graph",
    "gnmk_random_graph",
    "complete_bipartite_graph",
]

@_dispatchable
def complete_bipartite_graph(n1, n2, create_using: Graph[_Node] | type[Graph[_Node]] | None = None): ...
@_dispatchable
def configuration_model(
    aseq: Iterable[Incomplete],
    bseq: Iterable[Incomplete],
    create_using: Graph[_Node] | type[Graph[_Node]] | None = None,
    seed: int | RandomState | None = None,
):
    """
    Returns a random bipartite graph from two given degree sequences.

    Parameters
    ----------
    aseq : list
       Degree sequence for node set A.
    bseq : list
       Degree sequence for node set B.
    create_using : NetworkX graph instance, optional
       Return graph of this type.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    The graph is composed of two partitions. Set A has nodes 0 to
    (len(aseq) - 1) and set B has nodes len(aseq) to (len(bseq) - 1).
    Nodes from set A are connected to nodes in set B by choosing
    randomly from the possible free stubs, one in A and one in B.

    Notes
    -----
    The sum of the two sequences must be equal: sum(aseq)=sum(bseq)
    If no graph type is specified use MultiGraph with parallel edges.
    If you want a graph with no parallel edges use create_using=Graph()
    but then the resulting degree sequences might not be exact.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.configuration_model
    """
    ...
@_dispatchable
def havel_hakimi_graph(
    aseq: Iterable[Incomplete], bseq: Iterable[Incomplete], create_using: Graph[_Node] | type[Graph[_Node]] | None = None
): ...
@_dispatchable
def reverse_havel_hakimi_graph(
    aseq: Iterable[Incomplete], bseq: Iterable[Incomplete], create_using: Graph[_Node] | type[Graph[_Node]] | None = None
): ...
@_dispatchable
def alternating_havel_hakimi_graph(
    aseq: Iterable[Incomplete], bseq: Iterable[Incomplete], create_using: Graph[_Node] | type[Graph[_Node]] | None = None
): ...
@_dispatchable
def preferential_attachment_graph(
    aseq: Iterable[Incomplete],
    p: float,
    create_using: Graph[_Node] | type[Graph[_Node]] | None = None,
    seed: int | RandomState | None = None,
): ...
@_dispatchable
def random_graph(n: int, m: int, p: float, seed: int | RandomState | None = None, directed: bool | None = False):
    """
    Returns a bipartite random graph.

    This is a bipartite version of the binomial (Erdős-Rényi) graph.
    The graph is composed of two partitions. Set A has nodes 0 to
    (n - 1) and set B has nodes n to (n + m - 1).

    Parameters
    ----------
    n : int
        The number of nodes in the first bipartite set.
    m : int
        The number of nodes in the second bipartite set.
    p : float
        Probability for edge creation.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True return a directed graph

    Notes
    -----
    The bipartite random graph algorithm chooses each of the n*m (undirected)
    or 2*nm (directed) possible edges with probability p.

    This algorithm is $O(n+m)$ where $m$ is the expected number of edges.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.random_graph

    See Also
    --------
    gnp_random_graph, configuration_model

    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """
    ...
@_dispatchable
def gnmk_random_graph(n: int, m: int, k: int, seed: int | RandomState | None = None, directed: bool | None = False):
    """
    Returns a random bipartite graph G_{n,m,k}.

    Produces a bipartite graph chosen randomly out of the set of all graphs
    with n top nodes, m bottom nodes, and k edges.
    The graph is composed of two sets of nodes.
    Set A has nodes 0 to (n - 1) and set B has nodes n to (n + m - 1).

    Parameters
    ----------
    n : int
        The number of nodes in the first bipartite set.
    m : int
        The number of nodes in the second bipartite set.
    k : int
        The number of edges
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True return a directed graph

    Examples
    --------
    >>> G = nx.bipartite.gnmk_random_graph(10, 20, 50)

    See Also
    --------
    gnm_random_graph

    Notes
    -----
    If k > m * n then a complete bipartite graph is returned.

    This graph is a bipartite version of the `G_{nm}` random graph model.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.gnmk_random_graph
    """
    ...
