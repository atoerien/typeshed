from _typeshed import Incomplete, Unused
from collections.abc import Generator, Iterable, Mapping, MutableSet, Reversible
from decimal import Decimal
from typing import NoReturn

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _EdgePlus, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["check_planarity", "is_planar", "PlanarEmbedding"]

@_dispatchable
def is_planar(G: Graph[_Node]) -> bool:
    """
    Returns True if and only if `G` is planar.

    A graph is *planar* iff it can be drawn in a plane without
    any edge intersections.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
       Whether the graph is planar.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2)])
    >>> nx.is_planar(G)
    True
    >>> nx.is_planar(nx.complete_graph(5))
    False

    See Also
    --------
    check_planarity :
        Check if graph is planar *and* return a `PlanarEmbedding` instance if True.
    """
    ...
@_dispatchable
def check_planarity(G: Graph[_Node], counterexample: bool = False):
    """
    Check if a graph is planar and return a counterexample or an embedding.

    A graph is planar iff it can be drawn in a plane without
    any edge intersections.

    Parameters
    ----------
    G : NetworkX graph
    counterexample : bool
        A Kuratowski subgraph (to proof non planarity) is only returned if set
        to true.

    Returns
    -------
    (is_planar, certificate) : (bool, NetworkX graph) tuple
        is_planar is true if the graph is planar.
        If the graph is planar `certificate` is a PlanarEmbedding
        otherwise it is a Kuratowski subgraph.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2)])
    >>> is_planar, P = nx.check_planarity(G)
    >>> print(is_planar)
    True

    When `G` is planar, a `PlanarEmbedding` instance is returned:

    >>> P.get_data()
    {0: [1, 2], 1: [0], 2: [0]}

    Notes
    -----
    A (combinatorial) embedding consists of cyclic orderings of the incident
    edges at each vertex. Given such an embedding there are multiple approaches
    discussed in literature to drawing the graph (subject to various
    constraints, e.g. integer coordinates), see e.g. [2].

    The planarity check algorithm and extraction of the combinatorial embedding
    is based on the Left-Right Planarity Test [1].

    A counterexample is only generated if the corresponding parameter is set,
    because the complexity of the counterexample generation is higher.

    See also
    --------
    is_planar :
        Check for planarity without creating a `PlanarEmbedding` or counterexample.

    References
    ----------
    .. [1] Ulrik Brandes:
        The Left-Right Planarity Test
        2009
        http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.217.9208
    .. [2] Takao Nishizeki, Md Saidur Rahman:
        Planar graph drawing
        Lecture Notes Series on Computing: Volume 12
        2004
    """
    ...
@_dispatchable
def get_counterexample(G: Graph[_Node]) -> Graph[_Node]:
    """
    Obtains a Kuratowski subgraph.

    Raises nx.NetworkXException if G is planar.

    The function removes edges such that the graph is still not planar.
    At some point the removal of any edge would make the graph planar.
    This subgraph must be a Kuratowski subgraph.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    subgraph : NetworkX graph
        A Kuratowski subgraph that proves that G is not planar.
    """
    ...
@_dispatchable
def get_counterexample_recursive(G: Graph[_Node]) -> Graph[_Node]:
    """Recursive version of :meth:`get_counterexample`."""
    ...

class Interval:
    """
    Represents a set of return edges.

    All return edges in an interval induce a same constraint on the contained
    edges, which means that all edges must either have a left orientation or
    all edges must have a right orientation.
    """
    low: Incomplete
    high: Incomplete

    def __init__(self, low=None, high=None) -> None: ...
    def empty(self):
        """Check if the interval is empty"""
        ...
    def copy(self):
        """Returns a copy of this interval"""
        ...
    def conflicting(self, b, planarity_state):
        """Returns True if interval I conflicts with edge b"""
        ...

class ConflictPair:
    """
    Represents a different constraint between two intervals.

    The edges in the left interval must have a different orientation than
    the one in the right interval.
    """
    left: Incomplete
    right: Incomplete

    def __init__(self, left=..., right=...) -> None: ...
    def swap(self) -> None:
        """Swap left and right intervals"""
        ...
    def lowest(self, planarity_state):
        """Returns the lowest lowpoint of a conflict pair"""
        ...

class LRPlanarity:
    """A class to maintain the state during planarity check."""
    __slots__ = [
        "G",
        "roots",
        "height",
        "lowpt",
        "lowpt2",
        "nesting_depth",
        "parent_edge",
        "DG",
        "adjs",
        "ordered_adjs",
        "ref",
        "side",
        "S",
        "stack_bottom",
        "lowpt_edge",
        "left_ref",
        "right_ref",
        "embedding",
    ]
    G: Incomplete
    roots: Incomplete
    height: Incomplete
    lowpt: Incomplete
    lowpt2: Incomplete
    nesting_depth: Incomplete
    parent_edge: Incomplete
    DG: Incomplete
    adjs: Incomplete
    ordered_adjs: Incomplete
    ref: Incomplete
    side: Incomplete
    S: Incomplete
    stack_bottom: Incomplete
    lowpt_edge: Incomplete
    left_ref: Incomplete
    right_ref: Incomplete
    embedding: Incomplete

    def __init__(self, G: Graph[_Node]) -> None: ...
    def lr_planarity(self) -> PlanarEmbedding[Incomplete] | None:
        """
        Execute the LR planarity test.

        Returns
        -------
        embedding : dict
            If the graph is planar an embedding is returned. Otherwise None.
        """
        ...
    def lr_planarity_recursive(self):
        """Recursive version of :meth:`lr_planarity`."""
        ...
    def dfs_orientation(self, v):
        """Orient the graph by DFS, compute lowpoints and nesting order."""
        ...
    def dfs_orientation_recursive(self, v) -> None:
        """Recursive version of :meth:`dfs_orientation`."""
        ...
    def dfs_testing(self, v):
        """Test for LR partition."""
        ...
    def dfs_testing_recursive(self, v):
        """Recursive version of :meth:`dfs_testing`."""
        ...
    def add_constraints(self, ei, e): ...
    def remove_back_edges(self, e) -> None: ...
    def dfs_embedding(self, v):
        """Completes the embedding."""
        ...
    def dfs_embedding_recursive(self, v) -> None:
        """Recursive version of :meth:`dfs_embedding`."""
        ...
    def sign(self, e):
        """Resolve the relative side of an edge to the absolute side."""
        ...
    def sign_recursive(self, e):
        """Recursive version of :meth:`sign`."""
        ...

# NOTE: Graph subclasses relationships are so complex
# we're only overriding methods that differ in signature from the base classes
# to use inheritance to our advantage and reduce complexity
class PlanarEmbedding(DiGraph[_Node]):
    """
    Represents a planar graph with its planar embedding.

    The planar embedding is given by a `combinatorial embedding
    <https://en.wikipedia.org/wiki/Graph_embedding#Combinatorial_embedding>`_.

    .. note:: `check_planarity` is the preferred way to check if a graph is planar.

    **Neighbor ordering:**

    In comparison to a usual graph structure, the embedding also stores the
    order of all neighbors for every vertex.
    The order of the neighbors can be given in clockwise (cw) direction or
    counterclockwise (ccw) direction. This order is stored as edge attributes
    in the underlying directed graph. For the edge (u, v) the edge attribute
    'cw' is set to the neighbor of u that follows immediately after v in
    clockwise direction.

    In order for a PlanarEmbedding to be valid it must fulfill multiple
    conditions. It is possible to check if these conditions are fulfilled with
    the method :meth:`check_structure`.
    The conditions are:

    * Edges must go in both directions (because the edge attributes differ)
    * Every edge must have a 'cw' and 'ccw' attribute which corresponds to a
      correct planar embedding.

    As long as a PlanarEmbedding is invalid only the following methods should
    be called:

    * :meth:`add_half_edge`
    * :meth:`connect_components`

    Even though the graph is a subclass of nx.DiGraph, it can still be used
    for algorithms that require undirected graphs, because the method
    :meth:`is_directed` is overridden. This is possible, because a valid
    PlanarGraph must have edges in both directions.

    **Half edges:**

    In methods like `add_half_edge` the term "half-edge" is used, which is
    a term that is used in `doubly connected edge lists
    <https://en.wikipedia.org/wiki/Doubly_connected_edge_list>`_. It is used
    to emphasize that the edge is only in one direction and there exists
    another half-edge in the opposite direction.
    While conventional edges always have two faces (including outer face) next
    to them, it is possible to assign each half-edge *exactly one* face.
    For a half-edge (u, v) that is oriented such that u is below v then the
    face that belongs to (u, v) is to the right of this half-edge.

    See Also
    --------
    is_planar :
        Preferred way to check if an existing graph is planar.

    check_planarity :
        A convenient way to create a `PlanarEmbedding`. If not planar,
        it returns a subgraph that shows this.

    Examples
    --------

    Create an embedding of a star graph (compare `nx.star_graph(3)`):

    >>> G = nx.PlanarEmbedding()
    >>> G.add_half_edge(0, 1)
    >>> G.add_half_edge(0, 2, ccw=1)
    >>> G.add_half_edge(0, 3, ccw=2)
    >>> G.add_half_edge(1, 0)
    >>> G.add_half_edge(2, 0)
    >>> G.add_half_edge(3, 0)

    Alternatively the same embedding can also be defined in counterclockwise
    orientation. The following results in exactly the same PlanarEmbedding:

    >>> G = nx.PlanarEmbedding()
    >>> G.add_half_edge(0, 1)
    >>> G.add_half_edge(0, 3, cw=1)
    >>> G.add_half_edge(0, 2, cw=3)
    >>> G.add_half_edge(1, 0)
    >>> G.add_half_edge(2, 0)
    >>> G.add_half_edge(3, 0)

    After creating a graph, it is possible to validate that the PlanarEmbedding
    object is correct:

    >>> G.check_structure()
    """
    def get_data(self) -> dict[_Node, list[_Node]]:
        """
        Converts the adjacency structure into a better readable structure.

        Returns
        -------
        embedding : dict
            A dict mapping all nodes to a list of neighbors sorted in
            clockwise order.

        See Also
        --------
        set_data
        """
        ...
    def set_data(self, data: Mapping[_Node, Reversible[_Node]]) -> None:
        """
        Inserts edges according to given sorted neighbor list.

        The input format is the same as the output format of get_data().

        Parameters
        ----------
        data : dict
            A dict mapping all nodes to a list of neighbors sorted in
            clockwise order.

        See Also
        --------
        get_data
        """
        ...
    def neighbors_cw_order(self, v: _Node) -> Generator[_Node, None, None]:
        """
        Generator for the neighbors of v in clockwise order.

        Parameters
        ----------
        v : node

        Yields
        ------
        node
        """
        ...
    def add_half_edge(self, start_node: _Node, end_node: _Node, *, cw: _Node | None = None, ccw: _Node | None = None):
        """
        Adds a half-edge from `start_node` to `end_node`.

        If the half-edge is not the first one out of `start_node`, a reference
        node must be provided either in the clockwise (parameter `cw`) or in
        the counterclockwise (parameter `ccw`) direction. Only one of `cw`/`ccw`
        can be specified (or neither in the case of the first edge).
        Note that specifying a reference in the clockwise (`cw`) direction means
        inserting the new edge in the first counterclockwise position with
        respect to the reference (and vice-versa).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        cw, ccw: node
            End node of reference edge.
            Omit or pass `None` if adding the first out-half-edge of `start_node`.


        Raises
        ------
        NetworkXException
            If the `cw` or `ccw` node is not a successor of `start_node`.
            If `start_node` has successors, but neither `cw` or `ccw` is provided.
            If both `cw` and `ccw` are specified.

        See Also
        --------
        connect_components
        """
        ...
    def check_structure(self) -> None:
        """
        Runs without exceptions if this object is valid.

        Checks that the following properties are fulfilled:

        * Edges go in both directions (because the edge attributes differ).
        * Every edge has a 'cw' and 'ccw' attribute which corresponds to a
          correct planar embedding.

        Running this method verifies that the underlying Graph must be planar.

        Raises
        ------
        NetworkXException
            This exception is raised with a short explanation if the
            PlanarEmbedding is invalid.
        """
        ...
    def add_half_edge_ccw(self, start_node: _Node, end_node: _Node, reference_neighbor: _Node) -> None:
        """
        Adds a half-edge from start_node to end_node.

        The half-edge is added counter clockwise next to the existing half-edge
        (start_node, reference_neighbor).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        reference_neighbor: node
            End node of reference edge.

        Raises
        ------
        NetworkXException
            If the reference_neighbor does not exist.

        See Also
        --------
        add_half_edge
        add_half_edge_cw
        connect_components
        """
        ...
    def add_half_edge_cw(self, start_node: _Node, end_node: _Node, reference_neighbor: _Node) -> None:
        """
        Adds a half-edge from start_node to end_node.

        The half-edge is added clockwise next to the existing half-edge
        (start_node, reference_neighbor).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        reference_neighbor: node
            End node of reference edge.

        Raises
        ------
        NetworkXException
            If the reference_neighbor does not exist.

        See Also
        --------
        add_half_edge
        add_half_edge_ccw
        connect_components
        """
        ...
    def connect_components(self, v: _Node, w: _Node) -> None:
        """
        Adds half-edges for (v, w) and (w, v) at some position.

        This method should only be called if v and w are in different
        components, or it might break the embedding.
        This especially means that if `connect_components(v, w)`
        is called it is not allowed to call `connect_components(w, v)`
        afterwards. The neighbor orientations in both directions are
        all set correctly after the first call.

        Parameters
        ----------
        v : node
        w : node

        See Also
        --------
        add_half_edge
        """
        ...
    def add_half_edge_first(self, start_node: _Node, end_node: _Node) -> None:
        """
        Add a half-edge and set end_node as start_node's leftmost neighbor.

        The new edge is inserted counterclockwise with respect to the current
        leftmost neighbor, if there is one.

        Parameters
        ----------
        start_node : node
        end_node : node

        See Also
        --------
        add_half_edge
        connect_components
        """
        ...
    def next_face_half_edge(self, v: _Node, w: _Node) -> tuple[_Node, _Node]:
        """
        Returns the following half-edge left of a face.

        Parameters
        ----------
        v : node
        w : node

        Returns
        -------
        half-edge : tuple
        """
        ...
    def traverse_face(
        self, v: _Node, w: _Node, mark_half_edges: MutableSet[tuple[_Node, _Node]] | None = None
    ) -> list[_Node]:
        """
        Returns nodes on the face that belong to the half-edge (v, w).

        The face that is traversed lies to the right of the half-edge (in an
        orientation where v is below w).

        Optionally it is possible to pass a set to which all encountered half
        edges are added. Before calling this method, this set must not include
        any half-edges that belong to the face.

        Parameters
        ----------
        v : node
            Start node of half-edge.
        w : node
            End node of half-edge.
        mark_half_edges: set, optional
            Set to which all encountered half-edges are added.

        Returns
        -------
        face : list
            A list of nodes that lie on this face.
        """
        ...
    # Overriden in __init__ to always raise
    def add_edge(self, u_of_edge: _Node, v_of_edge: _Node, **attr: Unused) -> NoReturn:
        """
        Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        u_of_edge, v_of_edge : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        Adding an edge that already exists updates the edge data.

        Many NetworkX algorithms designed for weighted graphs use
        an edge attribute (by default `weight`) to hold a numerical value.

        Examples
        --------
        The following all add the edge e=(1, 2) to graph G:

        >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> e = (1, 2)
        >>> G.add_edge(1, 2)  # explicit two-node form
        >>> G.add_edge(*e)  # single edge as tuple of two nodes
        >>> G.add_edges_from([(1, 2)])  # add edges from iterable container

        Associate data to edges using keywords:

        >>> G.add_edge(1, 2, weight=3)
        >>> G.add_edge(1, 3, weight=7, capacity=15, length=342.7)

        For non-string attribute keys, use subscript notation.

        >>> G.add_edge(1, 2)
        >>> G[1][2].update({0: 5})
        >>> G.edges[1, 2].update({0: 5})
        """
        ...
    def add_edges_from(self, ebunch_to_add: Iterable[_EdgePlus[_Node]], **attr: Unused) -> NoReturn:
        """
        Add all the edges in ebunch_to_add.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the container will be added to the
            graph. The edges must be given as 2-tuples (u, v) or
            3-tuples (u, v, d) where d is a dictionary containing edge data.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : add a single edge
        add_weighted_edges_from : convenient way to add weighted edges

        Notes
        -----
        Adding the same edge twice has no effect but any edge data
        will be updated when each duplicate edge is added.

        Edge attributes specified in an ebunch take precedence over
        attributes specified via keyword arguments.

        When adding edges from an iterator over the graph you are changing,
        a `RuntimeError` can be raised with message:
        `RuntimeError: dictionary changed size during iteration`. This
        happens when the graph's underlying dictionary is modified during
        iteration. To avoid this error, evaluate the iterator into a separate
        object, e.g. by using `list(iterator_of_edges)`, and pass this
        object to `G.add_edges_from`.

        Examples
        --------
        >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_edges_from([(0, 1), (1, 2)])  # using a list of edge tuples
        >>> e = zip(range(0, 3), range(1, 4))
        >>> G.add_edges_from(e)  # Add the path graph 0-1-2-3

        Associate data to edges

        >>> G.add_edges_from([(1, 2), (2, 3)], weight=3)
        >>> G.add_edges_from([(3, 4), (1, 4)], label="WN2898")

        Evaluate an iterator over a graph if using it to modify the same graph

        >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 4)])
        >>> # Grow graph by one new node, adding edges to all existing nodes.
        >>> # wrong way - will raise RuntimeError
        >>> # G.add_edges_from(((5, n) for n in G.nodes))
        >>> # right way - note that there will be no self-edge for node 5
        >>> G.add_edges_from(list((5, n) for n in G.nodes))
        """
        ...
    def add_weighted_edges_from(
        self, ebunch_to_add: Iterable[tuple[_Node, _Node, float | Decimal | None]], weight: str = "weight", **attr: Unused
    ) -> NoReturn:
        """
        Add weighted edges in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as 3-tuples (u, v, w)
            where w is a number.
        weight : string, optional (default= 'weight')
            The attribute name for the edge weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : add a single edge
        add_edges_from : add multiple edges

        Notes
        -----
        Adding the same edge twice for Graph/DiGraph simply updates
        the edge data. For MultiGraph/MultiDiGraph, duplicate edges
        are stored.

        When adding edges from an iterator over the graph you are changing,
        a `RuntimeError` can be raised with message:
        `RuntimeError: dictionary changed size during iteration`. This
        happens when the graph's underlying dictionary is modified during
        iteration. To avoid this error, evaluate the iterator into a separate
        object, e.g. by using `list(iterator_of_edges)`, and pass this
        object to `G.add_weighted_edges_from`.

        Examples
        --------
        >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_weighted_edges_from([(0, 1, 3.0), (1, 2, 7.5)])

        Evaluate an iterator over edges before passing it

        >>> G = nx.Graph([(1, 2), (2, 3), (3, 4)])
        >>> weight = 0.1
        >>> # Grow graph by one new node, adding edges to all existing nodes.
        >>> # wrong way - will raise RuntimeError
        >>> # G.add_weighted_edges_from(((5, n, weight) for n in G.nodes))
        >>> # correct way - note that there will be no self-edge for node 5
        >>> G.add_weighted_edges_from(list((5, n, weight) for n in G.nodes))
        """
        ...
