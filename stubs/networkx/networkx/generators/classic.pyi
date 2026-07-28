"""
Generators for some classic graphs.

The typical graph builder function is called as follows:

>>> G = nx.complete_graph(100)

returning the complete graph on n nodes labeled 0, .., 99
as a simple graph. Except for `empty_graph`, all the functions
in this module return a Graph class (i.e. a simple, undirected graph).
"""

from _typeshed import Incomplete
from collections.abc import Iterable

from networkx.classes import Graph
from networkx.utils.backends import _dispatchable

__all__ = [
    "balanced_tree",
    "barbell_graph",
    "binomial_tree",
    "complete_graph",
    "complete_multipartite_graph",
    "circular_ladder_graph",
    "circulant_graph",
    "cycle_graph",
    "dorogovtsev_goltsev_mendes_graph",
    "empty_graph",
    "full_rary_tree",
    "kneser_graph",
    "ladder_graph",
    "lollipop_graph",
    "null_graph",
    "path_graph",
    "star_graph",
    "tadpole_graph",
    "trivial_graph",
    "turan_graph",
    "wheel_graph",
]

@_dispatchable
def full_rary_tree(
    r: int, n: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def kneser_graph(n: int, k: int) -> Graph[Incomplete]: ...
@_dispatchable
def balanced_tree(
    r: int, h: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def barbell_graph(
    m1: int, m2: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def binomial_tree(n: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]: ...
@_dispatchable
def complete_graph(n: int | Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None): ...
@_dispatchable
def circular_ladder_graph(n, create_using=None):
    """
    Returns the circular ladder graph $CL_n$ of length n.

    $CL_n$ consists of two concentric n-cycles in which
    each of the n pairs of concentric nodes are joined by an edge.

    Node labels are the integers 0 to n-1

    .. plot::

        >>> nx.draw(nx.circular_ladder_graph(5))
    """
    ...
@_dispatchable
def circulant_graph(
    n: int, offsets: list[int], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def cycle_graph(n: int | Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None): ...
@_dispatchable
def dorogovtsev_goltsev_mendes_graph(
    n: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def empty_graph(
    n: Incomplete | int = 0,
    create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None,
    default: type[Graph[Incomplete]] = ...,
): ...
@_dispatchable
def ladder_graph(n, create_using=None):
    """
    Returns the Ladder graph of length n.

    This is two paths of n nodes, with
    each pair connected by a single edge.

    Node labels are the integers 0 to 2*n - 1.

    .. plot::

        >>> nx.draw(nx.ladder_graph(5))
    """
    ...
@_dispatchable
def lollipop_graph(m, n, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]: ...
@_dispatchable
def null_graph(create_using=None):
    """
    Returns the Null graph with no nodes or edges.

    See empty_graph for the use of create_using.
    """
    ...
@_dispatchable
def path_graph(n: int | Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None): ...
@_dispatchable
def star_graph(n: int | Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None): ...
@_dispatchable
def tadpole_graph(
    m, n, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete] | Incomplete: ...
@_dispatchable
def trivial_graph(create_using=None):
    """
    Return the Trivial graph with one node (with label 0) and no edges.

    .. plot::

        >>> nx.draw(nx.trivial_graph(), with_labels=True)
    """
    ...
@_dispatchable
def turan_graph(n: int, r: int): ...
@_dispatchable
def wheel_graph(n: int | Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None): ...
@_dispatchable
def complete_multipartite_graph(*subset_sizes) -> Graph[Incomplete]: ...
