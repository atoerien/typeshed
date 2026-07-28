"""
=================================
Travelling Salesman Problem (TSP)
=================================

Implementation of approximate algorithms
for solving and approximating the TSP problem.

Categories of algorithms which are implemented:

- Christofides (provides a 3/2-approximation of TSP)
- Greedy
- Simulated Annealing (SA)
- Threshold Accepting (TA)
- Asadpour Asymmetric Traveling Salesman Algorithm

The Travelling Salesman Problem tries to find, given the weight
(distance) between all points where a salesman has to visit, the
route so that:

- The total distance (cost) which the salesman travels is minimized.
- The salesman returns to the starting point.
- Note that for a complete graph, the salesman visits each point once.

The function `travelling_salesman_problem` allows for incomplete
graphs by finding all-pairs shortest paths, effectively converting
the problem to a complete graph problem. It calls one of the
approximate methods on that problem and then converts the result
back to the original graph using the previously found shortest paths.

TSP is an NP-hard problem in combinatorial optimization,
important in operations research and theoretical computer science.

http://en.wikipedia.org/wiki/Travelling_salesman_problem
"""

from _typeshed import Incomplete, SupportsLenAndGetItem
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal, TypeVar

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = [
    "traveling_salesman_problem",
    "christofides",
    "asadpour_atsp",
    "greedy_tsp",
    "simulated_annealing_tsp",
    "threshold_accepting_tsp",
]

_SupportsLenAndGetItemT = TypeVar("_SupportsLenAndGetItemT", bound=SupportsLenAndGetItem[Any])

def swap_two_nodes(soln: _SupportsLenAndGetItemT, seed) -> _SupportsLenAndGetItemT:
    """
    Swap two nodes in `soln` to give a neighbor solution.

    Parameters
    ----------
    soln : list of nodes
        Current cycle of nodes

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    list
        The solution after move is applied. (A neighbor solution.)

    Notes
    -----
        This function assumes that the incoming list `soln` is a cycle
        (that the first and last element are the same) and also that
        we don't want any move to change the first node in the list
        (and thus not the last node either).

        The input list is changed as well as returned. Make a copy if needed.

    See Also
    --------
        move_one_node
    """
    ...
def move_one_node(soln: _SupportsLenAndGetItemT, seed) -> _SupportsLenAndGetItemT:
    """
    Move one node to another position to give a neighbor solution.

    The node to move and the position to move to are chosen randomly.
    The first and last nodes are left untouched as soln must be a cycle
    starting at that node.

    Parameters
    ----------
    soln : list of nodes
        Current cycle of nodes

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    list
        The solution after move is applied. (A neighbor solution.)

    Notes
    -----
        This function assumes that the incoming list `soln` is a cycle
        (that the first and last element are the same) and also that
        we don't want any move to change the first node in the list
        (and thus not the last node either).

        The input list is changed as well as returned. Make a copy if needed.

    See Also
    --------
        swap_two_nodes
    """
    ...
@_dispatchable
def christofides(G: Graph[_Node], weight: str | None = "weight", tree: Graph[_Node] | None = None) -> list[Incomplete]:
    """
    Approximate a solution of the traveling salesman problem

    Compute a 3/2-approximation of the traveling salesman problem
    in a complete undirected graph using Christofides [1]_ algorithm.

    Parameters
    ----------
    G : Graph
        `G` should be a complete weighted undirected graph.
        The distance between all pairs of nodes should be included.

    weight : string, optional (default="weight")
        Edge data key corresponding to the edge weight.
        If any edge does not have this attribute the weight is set to 1.

    tree : NetworkX graph or None (default: None)
        A minimum spanning tree of G. Or, if None, the minimum spanning
        tree is computed using :func:`networkx.minimum_spanning_tree`

    Returns
    -------
    list
        List of nodes in `G` along a cycle with a 3/2-approximation of
        the minimal Hamiltonian cycle.

    References
    ----------
    .. [1] Christofides, Nicos. "Worst-case analysis of a new heuristic for
       the travelling salesman problem." No. RR-388. Carnegie-Mellon Univ
       Pittsburgh Pa Management Sciences Research Group, 1976.
    """
    ...
@_dispatchable
def traveling_salesman_problem(
    G: Graph[_Node],
    weight: str = "weight",
    nodes=None,
    cycle: bool = True,
    method: Callable[..., Incomplete] | None = None,
    **kwargs,
) -> list[Incomplete]: ...
@_dispatchable
def asadpour_atsp(
    G: DiGraph[_Node], weight: str | None = "weight", seed: int | RandomState | None = None, source: str | None = None
) -> list[Incomplete]: ...
@_dispatchable
def held_karp_ascent(
    G: Graph[_Node], weight: str = "weight"
) -> tuple[float, dict[Incomplete, Incomplete] | Graph[Incomplete]]: ...
@_dispatchable
def spanning_tree_distribution(G: Graph[_Node], z: Mapping[Incomplete, Incomplete]) -> dict[Incomplete, Incomplete]:
    """
    Find the asadpour exponential distribution of spanning trees.

    Solves the Maximum Entropy Convex Program in the Asadpour algorithm [1]_
    using the approach in section 7 to build an exponential distribution of
    undirected spanning trees.

    This algorithm ensures that the probability of any edge in a spanning
    tree is proportional to the sum of the probabilities of the tress
    containing that edge over the sum of the probabilities of all spanning
    trees of the graph.

    Parameters
    ----------
    G : nx.MultiGraph
        The undirected support graph for the Held Karp relaxation

    z : dict
        The output of `held_karp_ascent()`, a scaled version of the Held-Karp
        solution.

    Returns
    -------
    gamma : dict
        The probability distribution which approximately preserves the marginal
        probabilities of `z`.
    """
    ...
@_dispatchable
def greedy_tsp(G: Graph[_Node], weight: str | None = "weight", source=None) -> list[Incomplete]: ...
@_dispatchable
def simulated_annealing_tsp(
    G: Graph[_Node],
    init_cycle: Literal["greedy"] | Iterable[Incomplete],
    weight: str | None = "weight",
    source=None,
    temp: int | None = 100,
    move: Callable[..., Incomplete] | Literal["1-1", "1-0"] = "1-1",
    max_iterations: int | None = 10,
    N_inner: int | None = 100,
    alpha: float = 0.01,
    seed: int | RandomState | None = None,
) -> list[Incomplete]: ...
@_dispatchable
def threshold_accepting_tsp(
    G: Graph[_Node],
    init_cycle: Literal["greedy"] | Iterable[Incomplete],
    weight: str | None = "weight",
    source=None,
    threshold: int | None = 1,
    move: Callable[..., Incomplete] | Literal["1-1", "1-0"] = "1-1",
    max_iterations: int | None = 10,
    N_inner: int | None = 100,
    alpha: float = 0.1,
    seed: int | RandomState | None = None,
) -> list[Incomplete]: ...
