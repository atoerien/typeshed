"""Algorithms for calculating min/max spanning trees/forests."""

from _typeshed import Incomplete
from collections.abc import Callable, Generator, Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Final, Literal
from typing_extensions import Self

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = [
    "minimum_spanning_edges",
    "maximum_spanning_edges",
    "minimum_spanning_tree",
    "maximum_spanning_tree",
    "number_of_spanning_trees",
    "random_spanning_tree",
    "partition_spanning_tree",
    "EdgePartition",
    "SpanningTreeIterator",
]

class EdgePartition(Enum):
    """
    An enum to store the state of an edge partition. The enum is written to the
    edges of a graph before being pasted to `kruskal_mst_edges`. Options are:

    - EdgePartition.OPEN
    - EdgePartition.INCLUDED
    - EdgePartition.EXCLUDED
    """
    OPEN = 0
    INCLUDED = 1
    EXCLUDED = 2

@_dispatchable
def boruvka_mst_edges(
    G: Graph[_Node], minimum: bool = True, weight: str = "weight", keys: bool = False, data: bool = True, ignore_nan: bool = False
): ...
@_dispatchable
def kruskal_mst_edges(
    G: Graph[_Node],
    minimum: bool,
    weight: str = "weight",
    keys: bool = True,
    data: bool = True,
    ignore_nan: bool = False,
    partition: str | None = None,
): ...
@_dispatchable
def prim_mst_edges(
    G: Graph[_Node], minimum: bool, weight: str = "weight", keys: bool = True, data: bool = True, ignore_nan: bool = False
): ...

ALGORITHMS: Final[dict[str, Callable[..., Generator[Incomplete, Incomplete, Incomplete]]]]

@_dispatchable
def minimum_spanning_edges(
    G: Graph[_Node],
    algorithm: str = "kruskal",
    weight: str = "weight",
    keys: bool = True,
    data: bool | None = True,
    ignore_nan: bool = False,
) -> Iterator[Incomplete]: ...
@_dispatchable
def maximum_spanning_edges(
    G: Graph[_Node],
    algorithm: str = "kruskal",
    weight: str = "weight",
    keys: bool = True,
    data: bool | None = True,
    ignore_nan: bool = False,
) -> Iterator[Incomplete]: ...
@_dispatchable
def minimum_spanning_tree(
    G: Graph[_Node], weight: str = "weight", algorithm: str = "kruskal", ignore_nan: bool = False
) -> Graph[Incomplete]: ...
@_dispatchable
def partition_spanning_tree(
    G: Graph[_Node], minimum: bool = True, weight: str = "weight", partition: str = "partition", ignore_nan: bool = False
) -> Graph[Incomplete]: ...
@_dispatchable
def maximum_spanning_tree(
    G: Graph[_Node], weight: str = "weight", algorithm: str = "kruskal", ignore_nan: bool = False
) -> Graph[Incomplete]: ...
@_dispatchable
def random_spanning_tree(
    G: Graph[_Node], weight: str | None = None, *, multiplicative=True, seed: int | RandomState | None = None
) -> Graph[Incomplete]: ...

class SpanningTreeIterator:
    """
    Iterate over all spanning trees of a graph in either increasing or
    decreasing cost.

    Notes
    -----
    This iterator uses the partition scheme from [1]_ (included edges,
    excluded edges and open edges) as well as a modified Kruskal's Algorithm
    to generate minimum spanning trees which respect the partition of edges.
    For spanning trees with the same weight, ties are broken arbitrarily.

    References
    ----------
    .. [1] G.K. Janssens, K. Sörensen, An algorithm to generate all spanning
           trees in order of increasing cost, Pesquisa Operacional, 2005-08,
           Vol. 25 (2), p. 219-229,
           https://www.scielo.br/j/pope/a/XHswBwRwJyrfL88dmMwYNWp/?lang=en
    """
    @dataclass(order=True)
    class Partition:
        """
        This dataclass represents a partition and stores a dict with the edge
        data and the weight of the minimum spanning tree of the partition dict.
        """
        mst_weight: float
        partition_dict: dict[Incomplete, Incomplete]
        def __copy__(self) -> SpanningTreeIterator.Partition: ...

    G: Incomplete
    weight: Incomplete
    minimum: Incomplete
    ignore_nan: Incomplete
    partition_key: str

    def __init__(self, G: DiGraph[_Node], weight: str = "weight", minimum: bool = True, ignore_nan: bool = False) -> None:
        """
        Initialize the iterator

        Parameters
        ----------
        G : nx.Graph
            The directed graph which we need to iterate trees over

        weight : String, default = "weight"
            The edge attribute used to store the weight of the edge

        minimum : bool, default = True
            Return the trees in increasing order while true and decreasing order
            while false.

        ignore_nan : bool, default = False
            If a NaN is found as an edge weight normally an exception is raised.
            If `ignore_nan is True` then that edge is ignored instead.
        """
        ...
    partition_queue: Incomplete

    def __iter__(self) -> Self:
        """
        Returns
        -------
        SpanningTreeIterator
            The iterator object for this graph
        """
        ...
    def __next__(self):
        """
        Returns
        -------
        (multi)Graph
            The spanning tree of next greatest weight, which ties broken
            arbitrarily.
        """
        ...

@_dispatchable
def number_of_spanning_trees(G: Graph[_Node], *, root=None, weight=None) -> float | Literal[0]:
    """
    Returns the number of spanning trees in `G`.

    A spanning tree for an undirected graph is a tree that connects
    all nodes in the graph. For a directed graph, the analog of a
    spanning tree is called a (spanning) arborescence. The arborescence
    includes a unique directed path from the `root` node to each other node.
    The graph must be weakly connected, and the root must be a node
    that includes all nodes as successors [3]_. Note that to avoid
    discussing sink-roots and reverse-arborescences, we have reversed
    the edge orientation from [3]_ and use the in-degree laplacian.

    This function (when `weight` is `None`) returns the number of
    spanning trees for an undirected graph and the number of
    arborescences from a single root node for a directed graph.
    When `weight` is the name of an edge attribute which holds the
    weight value of each edge, the function returns the sum over
    all trees of the multiplicative weight of each tree. That is,
    the weight of the tree is the product of its edge weights.

    Kirchoff's Tree Matrix Theorem states that any cofactor of the
    Laplacian matrix of a graph is the number of spanning trees in the
    graph. (Here we use cofactors for a diagonal entry so that the
    cofactor becomes the determinant of the matrix with one row
    and its matching column removed.) For a weighted Laplacian matrix,
    the cofactor is the sum across all spanning trees of the
    multiplicative weight of each tree. That is, the weight of each
    tree is the product of its edge weights. The theorem is also
    known as Kirchhoff's theorem [1]_ and the Matrix-Tree theorem [2]_.

    For directed graphs, a similar theorem (Tutte's Theorem) holds with
    the cofactor chosen to be the one with row and column removed that
    correspond to the root. The cofactor is the number of arborescences
    with the specified node as root. And the weighted version gives the
    sum of the arborescence weights with root `root`. The arborescence
    weight is the product of its edge weights.

    Parameters
    ----------
    G : NetworkX graph

    root : node
       A node in the directed graph `G` that has all nodes as descendants.
       (This is ignored for undirected graphs.)

    weight : string or None, optional (default=None)
        The name of the edge attribute holding the edge weight.
        If `None`, then each edge is assumed to have a weight of 1.

    Returns
    -------
    Number
        Undirected graphs:
            The number of spanning trees of the graph `G`.
            Or the sum of all spanning tree weights of the graph `G`
            where the weight of a tree is the product of its edge weights.
        Directed graphs:
            The number of arborescences of `G` rooted at node `root`.
            Or the sum of all arborescence weights of the graph `G` with
            specified root where the weight of an arborescence is the product
            of its edge weights.

    Raises
    ------
    NetworkXPointlessConcept
        If `G` does not contain any nodes.

    NetworkXError
        If the graph `G` is directed and the root node
        is not specified or is not in G.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> round(nx.number_of_spanning_trees(G))
    125

    >>> G = nx.Graph()
    >>> G.add_edge(1, 2, weight=2)
    >>> G.add_edge(1, 3, weight=1)
    >>> G.add_edge(2, 3, weight=1)
    >>> round(nx.number_of_spanning_trees(G, weight="weight"))
    5

    Notes
    -----
    Self-loops are excluded. Multi-edges are contracted in one edge
    equal to the sum of the weights.

    References
    ----------
    .. [1] Wikipedia
       "Kirchhoff's theorem."
       https://en.wikipedia.org/wiki/Kirchhoff%27s_theorem
    .. [2] Kirchhoff, G. R.
        Über die Auflösung der Gleichungen, auf welche man
        bei der Untersuchung der linearen Vertheilung
        Galvanischer Ströme geführt wird
        Annalen der Physik und Chemie, vol. 72, pp. 497-508, 1847.
    .. [3] Margoliash, J.
        "Matrix-Tree Theorem for Directed Graphs"
        https://www.math.uchicago.edu/~may/VIGRE/VIGRE2010/REUPapers/Margoliash.pdf
    """
    ...
