"""
Find the k-cores of a graph.

The k-core is found by recursively pruning nodes with degrees less than k.

See the following references for details:

An O(m) Algorithm for Cores Decomposition of Networks
Vladimir Batagelj and Matjaz Zaversnik, 2003.
https://arxiv.org/abs/cs.DS/0310049

Generalized Cores
Vladimir Batagelj and Matjaz Zaversnik, 2002.
https://arxiv.org/pdf/cs/0202039

For directed graphs a more general notion is that of D-cores which
looks at (k, l) restrictions on (in, out) degree. The (k, k) D-core
is the k-core.

D-cores: Measuring Collaboration of Directed Graphs Based on Degeneracy
Christos Giatsidis, Dimitrios M. Thilikos, Michalis Vazirgiannis, ICDM 2011.
http://www.graphdegeneracy.org/dcores_ICDM_2011.pdf

Multi-scale structure and topological anomaly detection via a new network statistic: The onion decomposition
L. Hébert-Dufresne, J. A. Grochow, and A. Allard
Scientific Reports 6, 31708 (2016)
http://doi.org/10.1038/srep31708
"""

from _typeshed import Incomplete
from collections.abc import Mapping

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["core_number", "k_core", "k_shell", "k_crust", "k_corona", "k_truss", "onion_layers"]

@_dispatchable
def core_number(G: Graph[_Node]) -> dict[Incomplete, Incomplete]:
    """
    Returns the core number for each node.

    A k-core is a maximal subgraph that contains nodes of degree k or more.

    The core number of a node is the largest value k of a k-core containing
    that node.

    Parameters
    ----------
    G : NetworkX graph
       An undirected or directed graph

    Returns
    -------
    core_number : dictionary
       A dictionary keyed by node to the core number.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is a multigraph or contains self loops.

    Notes
    -----
    For directed graphs the node degree is defined to be the
    in-degree + out-degree.

    Examples
    --------
    >>> degrees = [0, 1, 2, 2, 2, 2, 3]
    >>> H = nx.havel_hakimi_graph(degrees)
    >>> nx.core_number(H)
    {0: 1, 1: 2, 2: 2, 3: 2, 4: 1, 5: 2, 6: 0}
    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(1, 2), (2, 1), (2, 3), (2, 4), (3, 4), (4, 3)])
    >>> nx.core_number(G)
    {1: 2, 2: 2, 3: 2, 4: 2}

    References
    ----------
    .. [1] An O(m) Algorithm for Cores Decomposition of Networks
       Vladimir Batagelj and Matjaz Zaversnik, 2003.
       https://arxiv.org/abs/cs.DS/0310049
    """
    ...
@_dispatchable
def k_core(
    G: Graph[_Node], k: int | None = None, core_number: Mapping[Incomplete, Incomplete] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def k_shell(
    G: Graph[_Node], k: int | None = None, core_number: Mapping[Incomplete, Incomplete] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def k_crust(
    G: Graph[_Node], k: int | None = None, core_number: Mapping[Incomplete, Incomplete] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def k_corona(G: Graph[_Node], k: int | None, core_number: Mapping[Incomplete, Incomplete] | None = None) -> Graph[Incomplete]: ...
@_dispatchable
def k_truss(G: Graph[_Node], k: int) -> Graph[Incomplete]: ...
@_dispatchable
def onion_layers(G: Graph[_Node]) -> dict[Incomplete, Incomplete]:
    """
    Returns the layer of each vertex in an onion decomposition of the graph.

    The onion decomposition refines the k-core decomposition by providing
    information on the internal organization of each k-shell. It is usually
    used alongside the `core numbers`.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph without self loops.

    Returns
    -------
    od_layers : dictionary
        A dictionary keyed by node to the onion layer. The layers are
        contiguous integers starting at 1.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is a multigraph or directed graph or if it contains self loops.

    Examples
    --------
    >>> degrees = [0, 1, 2, 2, 2, 2, 3]
    >>> H = nx.havel_hakimi_graph(degrees)
    >>> H.degree
    DegreeView({0: 1, 1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 0})
    >>> nx.onion_layers(H)
    {6: 1, 0: 2, 4: 3, 1: 4, 2: 4, 3: 4, 5: 4}

    See Also
    --------
    core_number

    References
    ----------
    .. [1] Multi-scale structure and topological anomaly detection via a new
       network statistic: The onion decomposition
       L. Hébert-Dufresne, J. A. Grochow, and A. Allard
       Scientific Reports 6, 31708 (2016)
       http://doi.org/10.1038/srep31708
    .. [2] Percolation and the effective structure of complex networks
       A. Allard and L. Hébert-Dufresne
       Physical Review X 9, 011023 (2019)
       http://doi.org/10.1103/PhysRevX.9.011023
    """
    ...
