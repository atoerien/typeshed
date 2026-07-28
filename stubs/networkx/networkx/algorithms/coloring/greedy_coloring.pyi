"""Greedy graph coloring using various strategies."""

from _typeshed import Incomplete, Unused
from collections.abc import Callable, Generator
from typing import Final, Literal

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = [
    "greedy_color",
    "strategy_connected_sequential",
    "strategy_connected_sequential_bfs",
    "strategy_connected_sequential_dfs",
    "strategy_independent_set",
    "strategy_largest_first",
    "strategy_random_sequential",
    "strategy_saturation_largest_first",
    "strategy_smallest_last",
]

@_dispatchable
def strategy_largest_first(G: Graph[_Node], colors: Unused):
    """
    Returns a list of the nodes of ``G`` in decreasing order by
    degree.

    ``G`` is a NetworkX graph. ``colors`` is ignored.
    """
    ...
@_dispatchable
def strategy_random_sequential(G: Graph[_Node], colors: Unused, seed=None):
    """
    Returns a random permutation of the nodes of ``G`` as a list.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """
    ...
@_dispatchable
def strategy_smallest_last(G: Graph[_Node], colors: Unused):
    """
    Returns a deque of the nodes of ``G``, "smallest" last.

    Specifically, the degrees of each node are tracked in a bucket queue.
    From this, the node of minimum degree is repeatedly popped from the
    graph, updating its neighbors' degrees.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    This implementation of the strategy runs in $O(n + m)$ time
    (ignoring polylogarithmic factors), where $n$ is the number of nodes
    and $m$ is the number of edges.

    This strategy is related to :func:`strategy_independent_set`: if we
    interpret each node removed as an independent set of size one, then
    this strategy chooses an independent set of size one instead of a
    maximal independent set.
    """
    ...
@_dispatchable
def strategy_independent_set(G: Graph[_Node], colors: Unused) -> Generator[Incomplete, Incomplete]:
    """
    Uses a greedy independent set removal strategy to determine the
    colors.

    This function updates ``colors`` **in-place** and return ``None``,
    unlike the other strategy functions in this module.

    This algorithm repeatedly finds and removes a maximal independent
    set, assigning each node in the set an unused color.

    ``G`` is a NetworkX graph.

    This strategy is related to :func:`strategy_smallest_last`: in that
    strategy, an independent set of size one is chosen at each step
    instead of a maximal independent set.
    """
    ...
@_dispatchable
def strategy_connected_sequential_bfs(G: Graph[_Node], colors):
    """
    Returns an iterable over nodes in ``G`` in the order given by a
    breadth-first traversal.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.
    """
    ...
@_dispatchable
def strategy_connected_sequential_dfs(G: Graph[_Node], colors):
    """
    Returns an iterable over nodes in ``G`` in the order given by a
    depth-first traversal.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.
    """
    ...
@_dispatchable
def strategy_connected_sequential(G: Graph[_Node], colors: Unused, traversal: str = "bfs") -> Generator[Incomplete]:
    """
    Returns an iterable over nodes in ``G`` in the order given by a
    breadth-first or depth-first traversal.

    ``traversal`` must be one of the strings ``'dfs'`` or ``'bfs'``,
    representing depth-first traversal or breadth-first traversal,
    respectively.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.
    """
    ...
@_dispatchable
def strategy_saturation_largest_first(G: Graph[_Node], colors) -> Generator[Incomplete, None, Incomplete]:
    """
    Iterates over all the nodes of ``G`` in "saturation order" (also
    known as "DSATUR").

    ``G`` is a NetworkX graph. ``colors`` is a dictionary mapping nodes of
    ``G`` to colors, for those nodes that have already been colored.
    """
    ...

STRATEGIES: Final[dict[str, Callable[..., Incomplete]]]

@_dispatchable
def greedy_color(
    G: Graph[_Node],
    strategy: (
        Callable[..., Incomplete]
        | Literal[
            "largest_first",
            "random_sequential",
            "smallest_last",
            "independent_set",
            "connected_sequential_bfs",
            "connected_sequential_dfs",
            "connected_sequential",
            "saturation_largest_first",
            "DSATUR",
        ]
    ) = "largest_first",
    interchange: bool = False,
) -> dict[Incomplete, Incomplete]: ...
