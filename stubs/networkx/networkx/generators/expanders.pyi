from _typeshed import Incomplete
from typing_extensions import deprecated

from networkx.classes.graph import Graph, _Node
from networkx.classes.multigraph import MultiGraph
from networkx.utils.backends import _dispatchable

__all__ = [
    "margulis_gabber_galil_graph",
    "chordal_cycle_graph",
    "paley_graph",
    "maybe_regular_expander",
    "maybe_regular_expander_graph",
    "is_regular_expander",
    "random_regular_expander_graph",
]

@_dispatchable
def margulis_gabber_galil_graph(
    n: int, create_using: MultiGraph[Incomplete] | type[MultiGraph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
@_dispatchable
def chordal_cycle_graph(p: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]: ...
@_dispatchable
def paley_graph(p: int, create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None) -> Graph[Incomplete]: ...
@_dispatchable
def maybe_regular_expander_graph(n: int, d: int, *, create_using=None, max_tries: int = 100, seed=None) -> Graph[Incomplete]: ...
@deprecated(
    "`maybe_regular_expander` is a deprecated alias for `maybe_regular_expander_graph`. "
    "Use `maybe_regular_expander_graph` instead."
)
def maybe_regular_expander(n, d, *, create_using=None, max_tries: int = 100, seed=None):
    """
    .. deprecated:: 3.6
       `maybe_regular_expander` is a deprecated alias
       for `maybe_regular_expander_graph`.
       Use `maybe_regular_expander_graph` instead.
    """
    ...
@_dispatchable
def is_regular_expander(G: Graph[_Node], *, epsilon: float = 0) -> bool:
    r"""
    Determines whether the graph G is a regular expander. [1]_

    An expander graph is a sparse graph with strong connectivity properties.

    More precisely, this helper checks whether the graph is a
    regular $(n, d, \lambda)$-expander with $\lambda$ close to
    the Alon-Boppana bound and given by
    $\lambda = 2 \sqrt{d - 1} + \epsilon$. [2]_

    In the case where $\epsilon = 0$ then if the graph successfully passes the test
    it is a Ramanujan graph. [3]_

    A Ramanujan graph has spectral gap almost as large as possible, which makes them
    excellent expanders.

    Parameters
    ----------
    G : NetworkX graph
    epsilon : int, float, default=0

    Returns
    -------
    bool
        Whether the given graph is a regular $(n, d, \lambda)$-expander
        where $\lambda = 2 \sqrt{d - 1} + \epsilon$.

    Examples
    --------
    >>> G = nx.random_regular_expander_graph(20, 4)
    >>> nx.is_regular_expander(G)
    True

    See Also
    --------
    maybe_regular_expander_graph
    random_regular_expander_graph

    References
    ----------
    .. [1] Expander graph, https://en.wikipedia.org/wiki/Expander_graph
    .. [2] Alon-Boppana bound, https://en.wikipedia.org/wiki/Alon%E2%80%93Boppana_bound
    .. [3] Ramanujan graphs, https://en.wikipedia.org/wiki/Ramanujan_graph
    """
    ...
@_dispatchable
def random_regular_expander_graph(n: int, d: int, *, epsilon=0, create_using=None, max_tries=100, seed=None): ...
