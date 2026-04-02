"""
Algorithms for directed acyclic graphs (DAGs).

Note that most of these functions are only guaranteed to work for DAGs.
In general, these functions do not check for acyclic-ness, so it is up
to the user to check for that.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Generator, Iterable

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = [
    "descendants",
    "ancestors",
    "topological_sort",
    "lexicographical_topological_sort",
    "all_topological_sorts",
    "topological_generations",
    "is_directed_acyclic_graph",
    "is_aperiodic",
    "transitive_closure",
    "transitive_closure_dag",
    "transitive_reduction",
    "antichains",
    "dag_longest_path",
    "dag_longest_path_length",
    "dag_to_branching",
]

@_dispatchable
def descendants(G: Graph[_Node], source) -> set[_Node]:
    """
    Returns all nodes reachable from `source` in `G`.

    Parameters
    ----------
    G : NetworkX Graph
    source : node in `G`

    Returns
    -------
    set()
        The descendants of `source` in `G`

    Raises
    ------
    NetworkXError
        If node `source` is not in `G`.

    Examples
    --------
    >>> DG = nx.path_graph(5, create_using=nx.DiGraph)
    >>> sorted(nx.descendants(DG, 2))
    [3, 4]

    The `source` node is not a descendant of itself, but can be included manually:

    >>> sorted(nx.descendants(DG, 2) | {2})
    [2, 3, 4]

    See also
    --------
    ancestors
    """
    ...
@_dispatchable
def ancestors(G: Graph[_Node], source) -> set[_Node]:
    """
    Returns all nodes having a path to `source` in `G`.

    Parameters
    ----------
    G : NetworkX Graph
    source : node in `G`

    Returns
    -------
    set()
        The ancestors of `source` in `G`

    Raises
    ------
    NetworkXError
        If node `source` is not in `G`.

    Examples
    --------
    >>> DG = nx.path_graph(5, create_using=nx.DiGraph)
    >>> sorted(nx.ancestors(DG, 2))
    [0, 1]

    The `source` node is not an ancestor of itself, but can be included manually:

    >>> sorted(nx.ancestors(DG, 2) | {2})
    [0, 1, 2]

    See also
    --------
    descendants
    """
    ...
@_dispatchable
def is_directed_acyclic_graph(G: Graph[_Node]) -> bool:
    """
    Returns True if the graph `G` is a directed acyclic graph (DAG) or
    False if not.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        True if `G` is a DAG, False otherwise

    Examples
    --------
    Undirected graph::

        >>> G = nx.Graph([(1, 2), (2, 3)])
        >>> nx.is_directed_acyclic_graph(G)
        False

    Directed graph with cycle::

        >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
        >>> nx.is_directed_acyclic_graph(G)
        False

    Directed acyclic graph::

        >>> G = nx.DiGraph([(1, 2), (2, 3)])
        >>> nx.is_directed_acyclic_graph(G)
        True

    See also
    --------
    topological_sort
    """
    ...
@_dispatchable
def topological_generations(G: DiGraph[_Node]) -> Generator[list[_Node]]: ...
@_dispatchable
def topological_sort(G: DiGraph[_Node]) -> Generator[_Node]: ...
@_dispatchable
def lexicographical_topological_sort(G: DiGraph[_Node], key: Callable[..., Incomplete] | None = None) -> Generator[_Node]: ...
@_dispatchable
def all_topological_sorts(G: DiGraph[_Node]) -> Generator[list[_Node]]: ...
@_dispatchable
def is_aperiodic(G: DiGraph[_Node]) -> bool:
    """
    Returns True if `G` is aperiodic.

    A strongly connected directed graph is aperiodic if there is no integer ``k > 1``
    that divides the length of every cycle in the graph.

    This function requires the graph `G` to be strongly connected and will raise
    an error if it's not. For graphs that are not strongly connected, you should
    first identify their strongly connected components
    (using :func:`~networkx.algorithms.components.strongly_connected_components`)
    or attracting components
    (using :func:`~networkx.algorithms.components.attracting_components`),
    and then apply this function to those individual components.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed graph

    Returns
    -------
    bool
        True if the graph is aperiodic False otherwise

    Raises
    ------
    NetworkXError
        If `G` is not directed
    NetworkXError
        If `G` is not strongly connected
    NetworkXPointlessConcept
        If `G` has no nodes

    Examples
    --------
    A graph consisting of one cycle, the length of which is 2. Therefore ``k = 2``
    divides the length of every cycle in the graph and thus the graph
    is *not aperiodic*::

        >>> DG = nx.DiGraph([(1, 2), (2, 1)])
        >>> nx.is_aperiodic(DG)
        False

    A graph consisting of two cycles: one of length 2 and the other of length 3.
    The cycle lengths are coprime, so there is no single value of k where ``k > 1``
    that divides each cycle length and therefore the graph is *aperiodic*::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)])
        >>> nx.is_aperiodic(DG)
        True

    A graph created from cycles of the same length can still be aperiodic since
    the cycles can overlap and form new cycles of different lengths. For example,
    the following graph contains a cycle ``[4, 2, 3, 1]`` of length 4, which is coprime
    with the explicitly added cycles of length 3, so the graph is aperiodic::

        >>> DG = nx.DiGraph()
        >>> nx.add_cycle(DG, [1, 2, 3])
        >>> nx.add_cycle(DG, [2, 1, 4])
        >>> nx.is_aperiodic(DG)
        True

    A single-node graph's aperiodicity depends on whether it has a self-loop:
    it is aperiodic if a self-loop exists, and periodic otherwise::

        >>> G = nx.DiGraph()
        >>> G.add_node(1)
        >>> nx.is_aperiodic(G)
        False
        >>> G.add_edge(1, 1)
        >>> nx.is_aperiodic(G)
        True

    A Markov chain can be modeled as a directed graph, with nodes representing
    states and edges representing transitions with non-zero probability.
    Aperiodicity is typically considered for irreducible Markov chains,
    which are those that are *strongly connected* as graphs.

    The following Markov chain is irreducible and aperiodic, and thus
    ergodic. It is guaranteed to have a unique stationary distribution::

        >>> G = nx.DiGraph()
        >>> nx.add_cycle(G, [1, 2, 3, 4])
        >>> G.add_edge(1, 3)
        >>> nx.is_aperiodic(G)
        True

    Reducible Markov chains can sometimes have a unique stationary distribution.
    This occurs if the chain has exactly one closed communicating class and
    that class itself is aperiodic (see [1]_). You can use
    :func:`~networkx.algorithms.components.attracting_components`
    to find these closed communicating classes::

        >>> G = nx.DiGraph([(1, 3), (2, 3)])
        >>> nx.add_cycle(G, [3, 4, 5, 6])
        >>> nx.add_cycle(G, [3, 5, 6])
        >>> communicating_classes = list(nx.strongly_connected_components(G))
        >>> len(communicating_classes)
        3
        >>> closed_communicating_classes = list(nx.attracting_components(G))
        >>> len(closed_communicating_classes)
        1
        >>> nx.is_aperiodic(G.subgraph(closed_communicating_classes[0]))
        True

    Notes
    -----
    This uses the method outlined in [1]_, which runs in $O(m)$ time
    given $m$ edges in `G`.

    References
    ----------
    .. [1] Jarvis, J. P.; Shier, D. R. (1996),
       "Graph-theoretic analysis of finite Markov chains,"
       in Shier, D. R.; Wallenius, K. T., Applied Mathematical Modeling:
       A Multidisciplinary Approach, CRC Press.
    """
    ...
@_dispatchable
def transitive_closure(G: Graph[_Node], reflexive=False) -> Graph[_Node]:
    """
    Returns transitive closure of a graph

    The transitive closure of G = (V,E) is a graph G+ = (V,E+) such that
    for all v, w in V there is an edge (v, w) in E+ if and only if there
    is a path from v to w in G.

    Handling of paths from v to v has some flexibility within this definition.
    A reflexive transitive closure creates a self-loop for the path
    from v to v of length 0. The usual transitive closure creates a
    self-loop only if a cycle exists (a path from v to v with length > 0).
    We also allow an option for no self-loops.

    Parameters
    ----------
    G : NetworkX Graph
        A directed/undirected graph/multigraph.
    reflexive : Bool or None, optional (default: False)
        Determines when cycles create self-loops in the Transitive Closure.
        If True, trivial cycles (length 0) create self-loops. The result
        is a reflexive transitive closure of G.
        If False (the default) non-trivial cycles create self-loops.
        If None, self-loops are not created.

    Returns
    -------
    NetworkX graph
        The transitive closure of `G`

    Raises
    ------
    NetworkXError
        If `reflexive` not in `{None, True, False}`

    Examples
    --------
    The treatment of trivial (i.e. length 0) cycles is controlled by the
    `reflexive` parameter.

    Trivial (i.e. length 0) cycles do not create self-loops when
    ``reflexive=False`` (the default)::

        >>> DG = nx.DiGraph([(1, 2), (2, 3)])
        >>> TC = nx.transitive_closure(DG, reflexive=False)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (2, 3)])

    However, nontrivial (i.e. length greater than 0) cycles create self-loops
    when ``reflexive=False`` (the default)::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
        >>> TC = nx.transitive_closure(DG, reflexive=False)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (1, 1), (2, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)])

    Trivial cycles (length 0) create self-loops when ``reflexive=True``::

        >>> DG = nx.DiGraph([(1, 2), (2, 3)])
        >>> TC = nx.transitive_closure(DG, reflexive=True)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 1), (1, 3), (2, 3), (2, 2), (3, 3)])

    And the third option is not to create self-loops at all when ``reflexive=None``::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
        >>> TC = nx.transitive_closure(DG, reflexive=None)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2)])

    References
    ----------
    .. [1] https://www.ics.uci.edu/~eppstein/PADS/PartialOrder.py
    """
    ...
@_dispatchable
def transitive_closure_dag(G: DiGraph[_Node], topo_order: Iterable[Incomplete] | None = None) -> DiGraph[_Node]:
    """
    Returns the transitive closure of a directed acyclic graph.

    This function is faster than the function `transitive_closure`, but fails
    if the graph has a cycle.

    The transitive closure of G = (V,E) is a graph G+ = (V,E+) such that
    for all v, w in V there is an edge (v, w) in E+ if and only if there
    is a non-null path from v to w in G.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    topo_order: list or tuple, optional
        A topological order for G (if None, the function will compute one)

    Returns
    -------
    NetworkX DiGraph
        The transitive closure of `G`

    Raises
    ------
    NetworkXNotImplemented
        If `G` is not directed
    NetworkXUnfeasible
        If `G` has a cycle

    Examples
    --------
    >>> DG = nx.DiGraph([(1, 2), (2, 3)])
    >>> TC = nx.transitive_closure_dag(DG)
    >>> TC.edges()
    OutEdgeView([(1, 2), (1, 3), (2, 3)])

    Notes
    -----
    This algorithm is probably simple enough to be well-known but I didn't find
    a mention in the literature.
    """
    ...
@_dispatchable
def transitive_reduction(G: DiGraph[_Node]) -> DiGraph[_Node]:
    """
    Returns transitive reduction of a directed graph

    The transitive reduction of G = (V,E) is a graph G- = (V,E-) such that
    for all v,w in V there is an edge (v,w) in E- if and only if (v,w) is
    in E and there is no path from v to w in G with length greater than 1.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    Returns
    -------
    NetworkX DiGraph
        The transitive reduction of `G`

    Raises
    ------
    NetworkXError
        If `G` is not a directed acyclic graph (DAG) transitive reduction is
        not uniquely defined and a :exc:`NetworkXError` exception is raised.

    Examples
    --------
    To perform transitive reduction on a DiGraph:

    >>> DG = nx.DiGraph([(1, 2), (2, 3), (1, 3)])
    >>> TR = nx.transitive_reduction(DG)
    >>> list(TR.edges)
    [(1, 2), (2, 3)]

    To avoid unnecessary data copies, this implementation does not return a
    DiGraph with node/edge data.
    To perform transitive reduction on a DiGraph and transfer node/edge data:

    >>> DG = nx.DiGraph()
    >>> DG.add_edges_from([(1, 2), (2, 3), (1, 3)], color="red")
    >>> TR = nx.transitive_reduction(DG)
    >>> TR.add_nodes_from(DG.nodes(data=True))
    >>> TR.add_edges_from((u, v, DG.edges[u, v]) for u, v in TR.edges)
    >>> list(TR.edges(data=True))
    [(1, 2, {'color': 'red'}), (2, 3, {'color': 'red'})]

    References
    ----------
    https://en.wikipedia.org/wiki/Transitive_reduction
    """
    ...
@_dispatchable
def antichains(G: DiGraph[_Node], topo_order: Iterable[Incomplete] | None = None) -> Generator[list[_Node]]: ...
@_dispatchable
def dag_longest_path(
    G: DiGraph[_Node],
    weight: str | None = "weight",
    default_weight: int | None = 1,
    topo_order: Iterable[Incomplete] | None = None,
) -> list[_Node]:
    """
    Returns the longest path in a directed acyclic graph (DAG).

    If `G` has edges with `weight` attribute the edge data are used as
    weight values.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    weight : str, optional
        Edge data key to use for weight

    default_weight : int, optional
        The weight of edges that do not have a weight attribute

    topo_order: list or tuple, optional
        A topological order for `G` (if None, the function will compute one)

    Returns
    -------
    list
        Longest path

    Raises
    ------
    NetworkXNotImplemented
        If `G` is not directed

    Examples
    --------
    >>> DG = nx.DiGraph(
    ...     [(0, 1, {"cost": 1}), (1, 2, {"cost": 1}), (0, 2, {"cost": 42})]
    ... )
    >>> list(nx.all_simple_paths(DG, 0, 2))
    [[0, 1, 2], [0, 2]]
    >>> nx.dag_longest_path(DG)
    [0, 1, 2]
    >>> nx.dag_longest_path(DG, weight="cost")
    [0, 2]

    In the case where multiple valid topological orderings exist, `topo_order`
    can be used to specify a specific ordering:

    >>> DG = nx.DiGraph([(0, 1), (0, 2)])
    >>> sorted(nx.all_topological_sorts(DG))  # Valid topological orderings
    [[0, 1, 2], [0, 2, 1]]
    >>> nx.dag_longest_path(DG, topo_order=[0, 1, 2])
    [0, 1]
    >>> nx.dag_longest_path(DG, topo_order=[0, 2, 1])
    [0, 2]

    See also
    --------
    dag_longest_path_length
    """
    ...
@_dispatchable
def dag_longest_path_length(G: DiGraph[_Node], weight: str | None = "weight", default_weight: int | None = 1) -> int:
    """
    Returns the longest path length in a DAG

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    weight : string, optional
        Edge data key to use for weight

    default_weight : int, optional
        The weight of edges that do not have a weight attribute

    Returns
    -------
    int
        Longest path length

    Raises
    ------
    NetworkXNotImplemented
        If `G` is not directed

    Examples
    --------
    >>> DG = nx.DiGraph(
    ...     [(0, 1, {"cost": 1}), (1, 2, {"cost": 1}), (0, 2, {"cost": 42})]
    ... )
    >>> list(nx.all_simple_paths(DG, 0, 2))
    [[0, 1, 2], [0, 2]]
    >>> nx.dag_longest_path_length(DG)
    2
    >>> nx.dag_longest_path_length(DG, weight="cost")
    42

    See also
    --------
    dag_longest_path
    """
    ...
@_dispatchable
def dag_to_branching(G: DiGraph[_Node]) -> DiGraph[_Node]:
    """
    Returns a branching representing all (overlapping) paths from
    root nodes to leaf nodes in the given directed acyclic graph.

    As described in :mod:`networkx.algorithms.tree.recognition`, a
    *branching* is a directed forest in which each node has at most one
    parent. In other words, a branching is a disjoint union of
    *arborescences*. For this function, each node of in-degree zero in
    `G` becomes a root of one of the arborescences, and there will be
    one leaf node for each distinct path from that root to a leaf node
    in `G`.

    Each node `v` in `G` with *k* parents becomes *k* distinct nodes in
    the returned branching, one for each parent, and the sub-DAG rooted
    at `v` is duplicated for each copy. The algorithm then recurses on
    the children of each copy of `v`.

    Parameters
    ----------
    G : NetworkX graph
        A directed acyclic graph.

    Returns
    -------
    DiGraph
        The branching in which there is a bijection between root-to-leaf
        paths in `G` (in which multiple paths may share the same leaf)
        and root-to-leaf paths in the branching (in which there is a
        unique path from a root to a leaf).

        Each node has an attribute 'source' whose value is the original
        node to which this node corresponds. No other graph, node, or
        edge attributes are copied into this new graph.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is not directed, or if `G` is a multigraph.

    HasACycle
        If `G` is not acyclic.

    Examples
    --------
    To examine which nodes in the returned branching were produced by
    which original node in the directed acyclic graph, we can collect
    the mapping from source node to new nodes into a dictionary. For
    example, consider the directed diamond graph::

        >>> from collections import defaultdict
        >>> from operator import itemgetter
        >>>
        >>> G = nx.DiGraph(nx.utils.pairwise("abd"))
        >>> G.add_edges_from(nx.utils.pairwise("acd"))
        >>> B = nx.dag_to_branching(G)
        >>>
        >>> sources = defaultdict(set)
        >>> for v, source in B.nodes(data="source"):
        ...     sources[source].add(v)
        >>> len(sources["a"])
        1
        >>> len(sources["d"])
        2

    To copy node attributes from the original graph to the new graph,
    you can use a dictionary like the one constructed in the above
    example::

        >>> for source, nodes in sources.items():
        ...     for v in nodes:
        ...         B.nodes[v].update(G.nodes[source])

    Notes
    -----
    This function is not idempotent in the sense that the node labels in
    the returned branching may be uniquely generated each time the
    function is invoked. In fact, the node labels may not be integers;
    in order to relabel the nodes to be more readable, you can use the
    :func:`networkx.convert_node_labels_to_integers` function.

    The current implementation of this function uses
    :func:`networkx.prefix_tree`, so it is subject to the limitations of
    that function.
    """
    ...
