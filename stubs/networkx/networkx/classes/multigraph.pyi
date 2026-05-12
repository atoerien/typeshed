"""Base class for MultiGraph."""

from collections.abc import Hashable
from functools import cached_property
from typing import Any, ClassVar, TypeAlias, overload
from typing_extensions import Self, TypeVar

from networkx.classes.coreviews import MultiAdjacencyView
from networkx.classes.graph import Graph, _EdgeData, _MapFactory, _Node, _NodeData
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.reportviews import DiMultiDegreeView, MultiDegreeView, MultiEdgeView, OutMultiEdgeView

_MultiEdge: TypeAlias = tuple[_Node, _Node, int]  # noqa: Y047

_DefaultT = TypeVar("_DefaultT")
_KeyT = TypeVar("_KeyT", bound=Hashable)

__all__ = ["MultiGraph"]

# NOTE: Graph subclasses relationships are so complex
# we're only overriding methods that differ in signature from the base classes
# to use inheritance to our advantage and reduce complexity
class MultiGraph(Graph[_Node, _NodeData, _EdgeData]):
    edge_key_dict_factory: ClassVar[_MapFactory]
    def to_directed_class(self) -> type[MultiDiGraph[_Node, _NodeData, _EdgeData]]: ...
    def to_undirected_class(self) -> type[MultiGraph[_Node, _NodeData, _EdgeData]]: ...
    # @_dispatchable adds `backend` argument, but this decorated is unsupported constructor type here
    # and __init__() ignores this argument
    def __new__(cls, *args, backend=None, **kwargs) -> Self: ...
    def __init__(self, incoming_graph_data=None, multigraph_input: bool | None = None, **attr: Any) -> None:
        """
        Initialize a graph with edges, name, or graph attributes.

        Parameters
        ----------
        incoming_graph_data : input graph
            Data to initialize graph.  If incoming_graph_data=None (default)
            an empty graph is created.  The data can be an edge list, or any
            NetworkX graph object.  If the corresponding optional Python
            packages are installed the data can also be a 2D NumPy array, a
            SciPy sparse array, or a PyGraphviz graph.

        multigraph_input : bool or None (default None)
            Note: Only used when `incoming_graph_data` is a dict.
            If True, `incoming_graph_data` is assumed to be a
            dict-of-dict-of-dict-of-dict structure keyed by
            node to neighbor to edge keys to edge data for multi-edges.
            A NetworkXError is raised if this is not the case.
            If False, :func:`to_networkx_graph` is used to try to determine
            the dict's graph data structure as either a dict-of-dict-of-dict
            keyed by node to neighbor to edge data, or a dict-of-iterable
            keyed by node to neighbors.
            If None, the treatment for True is tried, but if it fails,
            the treatment for False is tried.

        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.

        See Also
        --------
        convert

        Examples
        --------
        >>> G = nx.MultiGraph()
        >>> G = nx.MultiGraph(name="my graph")
        >>> e = [(1, 2), (1, 2), (2, 3), (3, 4)]  # list of edges
        >>> G = nx.MultiGraph(e)

        Arbitrary graph attribute pairs (key=value) may be assigned

        >>> G = nx.MultiGraph(e, day="Friday")
        >>> G.graph
        {'day': 'Friday'}
        """
        ...
    @cached_property
    def adj(self) -> MultiAdjacencyView[_Node, _Node, _EdgeData]: ...  # data can be any type
    def new_edge_key(self, u: _Node, v: _Node) -> int: ...
    # key : hashable identifier, optional (default=lowest unused integer)
    @overload  # type: ignore[override] # More complex overload
    def add_edge(self, u_for_edge: _Node, v_for_edge: _Node, key: int | None = None, **attr: Any) -> int:
        """
        Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        u_for_edge, v_for_edge : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        key : hashable identifier, optional (default=lowest unused integer)
            Used to distinguish multiedges between a pair of nodes.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        Returns
        -------
        The edge key assigned to the edge.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        To replace/update edge data, use the optional key argument
        to identify a unique edge.  Otherwise a new edge will be created.

        NetworkX algorithms designed for weighted graphs cannot use
        multigraphs directly because it is not clear how to handle
        multiedge weights.  Convert to Graph using edge attribute
        'weight' to enable weighted graph algorithms.

        Default keys are generated using the method `new_edge_key()`.
        This method can be overridden by subclassing the base class and
        providing a custom `new_edge_key()` method.

        Examples
        --------
        The following each add an additional edge e=(1, 2) to graph G:

        >>> G = nx.MultiGraph()
        >>> e = (1, 2)
        >>> ekey = G.add_edge(1, 2)  # explicit two-node form
        >>> G.add_edge(*e)  # single edge as tuple of two nodes
        1
        >>> G.add_edges_from([(1, 2)])  # add edges from iterable container
        [2]

        Associate data to edges using keywords:

        >>> ekey = G.add_edge(1, 2, weight=3)
        >>> ekey = G.add_edge(1, 2, key=0, weight=4)  # update data for key=0
        >>> ekey = G.add_edge(1, 3, weight=7, capacity=15, length=342.7)

        For non-string attribute keys, use subscript notation.

        >>> ekey = G.add_edge(1, 2)
        >>> G[1][2][0].update({0: 5})
        >>> G.edges[1, 2, 0].update({0: 5})
        """
        ...
    @overload
    def add_edge(self, u_for_edge: _Node, v_for_edge: _Node, key: _KeyT, **attr: Any) -> _KeyT:
        """
        Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        u_for_edge, v_for_edge : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        key : hashable identifier, optional (default=lowest unused integer)
            Used to distinguish multiedges between a pair of nodes.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        Returns
        -------
        The edge key assigned to the edge.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        To replace/update edge data, use the optional key argument
        to identify a unique edge.  Otherwise a new edge will be created.

        NetworkX algorithms designed for weighted graphs cannot use
        multigraphs directly because it is not clear how to handle
        multiedge weights.  Convert to Graph using edge attribute
        'weight' to enable weighted graph algorithms.

        Default keys are generated using the method `new_edge_key()`.
        This method can be overridden by subclassing the base class and
        providing a custom `new_edge_key()` method.

        Examples
        --------
        The following each add an additional edge e=(1, 2) to graph G:

        >>> G = nx.MultiGraph()
        >>> e = (1, 2)
        >>> ekey = G.add_edge(1, 2)  # explicit two-node form
        >>> G.add_edge(*e)  # single edge as tuple of two nodes
        1
        >>> G.add_edges_from([(1, 2)])  # add edges from iterable container
        [2]

        Associate data to edges using keywords:

        >>> ekey = G.add_edge(1, 2, weight=3)
        >>> ekey = G.add_edge(1, 2, key=0, weight=4)  # update data for key=0
        >>> ekey = G.add_edge(1, 3, weight=7, capacity=15, length=342.7)

        For non-string attribute keys, use subscript notation.

        >>> ekey = G.add_edge(1, 2)
        >>> G[1][2][0].update({0: 5})
        >>> G.edges[1, 2, 0].update({0: 5})
        """
        ...
    def remove_edge(self, u: _Node, v: _Node, key: Hashable | None = None) -> None:
        """
        Remove an edge between u and v.

        Parameters
        ----------
        u, v : nodes
            Remove an edge between nodes u and v.
        key : hashable identifier, optional (default=None)
            Used to distinguish multiple edges between a pair of nodes.
            If None, remove a single edge between u and v. If there are
            multiple edges, removes the last edge added in terms of
            insertion order.

        Raises
        ------
        NetworkXError
            If there is not an edge between u and v, or
            if there is no edge with the specified key.

        See Also
        --------
        remove_edges_from : remove a collection of edges

        Examples
        --------
        >>> G = nx.MultiGraph()
        >>> nx.add_path(G, [0, 1, 2, 3])
        >>> G.remove_edge(0, 1)
        >>> e = (1, 2)
        >>> G.remove_edge(*e)  # unpacks e from an edge tuple

        For multiple edges

        >>> G = nx.MultiGraph()  # or MultiDiGraph, etc
        >>> G.add_edges_from([(1, 2), (1, 2), (1, 2)])  # key_list returned
        [0, 1, 2]

        When ``key=None`` (the default), edges are removed in the opposite
        order that they were added:

        >>> G.remove_edge(1, 2)
        >>> G.edges(keys=True)
        MultiEdgeView([(1, 2, 0), (1, 2, 1)])
        >>> G.remove_edge(2, 1)  # edges are not directed
        >>> G.edges(keys=True)
        MultiEdgeView([(1, 2, 0)])

        For edges with keys

        >>> G = nx.MultiGraph()
        >>> G.add_edge(1, 2, key="first")
        'first'
        >>> G.add_edge(1, 2, key="second")
        'second'
        >>> G.remove_edge(1, 2, key="first")
        >>> G.edges(keys=True)
        MultiEdgeView([(1, 2, 'second')])
        """
        ...
    def has_edge(self, u: _Node, v: _Node, key: Hashable | None = None) -> bool:
        """
        Returns True if the graph has an edge between nodes u and v.

        This is the same as `v in G[u] or key in G[u][v]`
        without KeyError exceptions.

        Parameters
        ----------
        u, v : nodes
            Nodes can be, for example, strings or numbers.

        key : hashable identifier, optional (default=None)
            If specified return True only if the edge with
            key is found.

        Returns
        -------
        edge_ind : bool
            True if edge is in the graph, False otherwise.

        Examples
        --------
        Can be called either using two nodes u, v, an edge tuple (u, v),
        or an edge tuple (u, v, key).

        >>> G = nx.MultiGraph()  # or MultiDiGraph
        >>> nx.add_path(G, [0, 1, 2, 3])
        >>> G.has_edge(0, 1)  # using two nodes
        True
        >>> e = (0, 1)
        >>> G.has_edge(*e)  #  e is a 2-tuple (u, v)
        True
        >>> G.add_edge(0, 1, key="a")
        'a'
        >>> G.has_edge(0, 1, key="a")  # specify key
        True
        >>> G.has_edge(1, 0, key="a")  # edges aren't directed
        True
        >>> e = (0, 1, "a")
        >>> G.has_edge(*e)  # e is a 3-tuple (u, v, 'a')
        True

        The following syntax are equivalent:

        >>> G.has_edge(0, 1)
        True
        >>> 1 in G[0]  # though this gives :exc:`KeyError` if 0 not in G
        True
        >>> 0 in G[1]  # other order; also gives :exc:`KeyError` if 0 not in G
        True
        """
        ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def edges(self) -> MultiEdgeView[_Node, _NodeData, _EdgeData] | OutMultiEdgeView[_Node, _NodeData, _EdgeData]: ...
    # key : hashable identifier, optional (default=None).
    # default : any Python object (default=None). Value to return if the specific edge (u, v, key) is not found.
    # Returns: The edge attribute dictionary.
    @overload  # type: ignore[override]
    def get_edge_data(self, u: _Node, v: _Node, key: Hashable, default: _DefaultT | None = None) -> _EdgeData | _DefaultT: ...
    # default : any Python object (default=None). Value to return if there are no edges between u and v and no key is specified.
    # Returns: A dictionary mapping edge keys to attribute dictionaries for each of those edges if no specific key is provided.
    @overload
    def get_edge_data(
        self, u: _Node, v: _Node, key: None = None, default: _DefaultT | None = None
    ) -> dict[Hashable, _EdgeData | _DefaultT]: ...
    def copy(self, as_view: bool = False) -> Self: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def degree(self) -> MultiDegreeView[_Node, _NodeData, _EdgeData] | DiMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    def to_directed(self, as_view: bool = False) -> MultiDiGraph[_Node, _NodeData, _EdgeData]: ...
    def to_undirected(self, as_view: bool = False) -> MultiGraph[_Node, _NodeData, _EdgeData]: ...
