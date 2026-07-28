"""
Algorithms for finding optimum branchings and spanning arborescences.

This implementation is based on:

    J. Edmonds, Optimum branchings, J. Res. Natl. Bur. Standards 71B (1967),
    233–240. URL: http://archive.org/details/jresv71Bn4p233
"""

from _typeshed import Incomplete
from dataclasses import dataclass
from typing import Final
from typing_extensions import Self

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = [
    "branching_weight",
    "greedy_branching",
    "maximum_branching",
    "minimum_branching",
    "minimal_branching",
    "maximum_spanning_arborescence",
    "minimum_spanning_arborescence",
    "ArborescenceIterator",
]

KINDS: Final[set[str]]
STYLES: Final[dict[str, str]]
INF: Final[float]

def random_string(L=15, seed=None): ...
@_dispatchable
def branching_weight(G: DiGraph[_Node], attr: str = "weight", default: float = 1) -> int | float: ...
@_dispatchable
def greedy_branching(
    G: DiGraph[_Node], attr: str = "weight", default: float = 1, kind: str = "max", seed: int | RandomState | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def maximum_branching(
    G: DiGraph[_Node], attr: str = "weight", default: float = 1, preserve_attrs: bool = False, partition: str | None = None
) -> DiGraph[Incomplete]: ...
@_dispatchable
def minimum_branching(
    G: DiGraph[_Node], attr: str = "weight", default: float = 1, preserve_attrs: bool = False, partition: str | None = None
) -> DiGraph[Incomplete]: ...
@_dispatchable
def minimal_branching(
    G: DiGraph[_Node], /, *, attr="weight", default=1, preserve_attrs=False, partition=None
) -> DiGraph[Incomplete]: ...
@_dispatchable
def maximum_spanning_arborescence(
    G: DiGraph[_Node], attr: str = "weight", default: float = 1, preserve_attrs: bool = False, partition: str | None = None
) -> DiGraph[Incomplete]: ...
@_dispatchable
def minimum_spanning_arborescence(
    G: DiGraph[_Node], attr: str = "weight", default: float = 1, preserve_attrs: bool = False, partition: str | None = None
) -> DiGraph[Incomplete]: ...

class ArborescenceIterator:
    """
    Iterate over all spanning arborescences of a graph in either increasing or
    decreasing cost.

    Notes
    -----
    This iterator uses the partition scheme from [1]_ (included edges,
    excluded edges and open edges). It generates minimum spanning
    arborescences using a modified Edmonds' Algorithm which respects the
    partition of edges. For arborescences with the same weight, ties are
    broken arbitrarily.

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
        data and the weight of the minimum spanning arborescence of the
        partition dict.
        """
        mst_weight: float
        partition_dict: dict[Incomplete, Incomplete]
        def __copy__(self) -> ArborescenceIterator.Partition: ...

    G: Incomplete
    weight: Incomplete
    minimum: Incomplete
    method: Incomplete
    partition_key: str
    init_partition: Incomplete

    def __init__(self, G: DiGraph[_Node], weight: str = "weight", minimum: bool = True, init_partition=None) -> None:
        """
        Initialize the iterator

        Parameters
        ----------
        G : nx.DiGraph
            The directed graph which we need to iterate trees over

        weight : String, default = "weight"
            The edge attribute used to store the weight of the edge

        minimum : bool, default = True
            Return the trees in increasing order while true and decreasing order
            while false.

        init_partition : tuple, default = None
            In the case that certain edges have to be included or excluded from
            the arborescences, `init_partition` should be in the form
            `(included_edges, excluded_edges)` where each edges is a
            `(u, v)`-tuple inside an iterable such as a list or set.
        """
        ...
    partition_queue: Incomplete

    def __iter__(self) -> Self:
        """
        Returns
        -------
        ArborescenceIterator
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
