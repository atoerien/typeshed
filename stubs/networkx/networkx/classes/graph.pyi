from collections.abc import Callable, Collection, Hashable, Iterable, Iterator, Mapping, MutableMapping
from decimal import Decimal
from functools import cached_property
from typing import Any, ClassVar, Generic, TypeAlias, TypeVar, overload
from typing_extensions import Self

import numpy
from networkx.classes.coreviews import AdjacencyView, AtlasView
from networkx.classes.digraph import DiGraph
from networkx.classes.reportviews import DegreeView, DiDegreeView, EdgeView, NodeView, OutEdgeView

_DataBound: TypeAlias = Mapping[str, Any]

_Node = TypeVar("_Node", bound=Hashable)
_NodeData = TypeVar("_NodeData", bound=_DataBound, default=dict[str, Any])
_EdgeData = TypeVar("_EdgeData", bound=_DataBound, default=dict[str, Any])

_NodeWithData: TypeAlias = tuple[_Node, _NodeData]
_NodePlus: TypeAlias = _Node | _NodeWithData[_Node, _NodeData]
_Edge: TypeAlias = tuple[_Node, _Node]
_EdgeWithData: TypeAlias = tuple[_Node, _Node, _EdgeData]
_EdgePlus: TypeAlias = _Edge[_Node] | _EdgeWithData[_Node, _EdgeData]
_MapFactory: TypeAlias = Callable[[], MutableMapping[str, Any]]
_NBunch: TypeAlias = _Node | Iterable[_Node] | None
_Data: TypeAlias = (
    Graph[_Node, _NodeData, _EdgeData]
    | dict[_Node, dict[_Node, _NodeData]]
    | dict[_Node, Iterable[_Node]]
    | Iterable[_EdgePlus[_Node, _EdgeData]]
    | numpy.ndarray[Any, Any]
    # | scipy.sparse.base.spmatrix
)

__all__ = ["Graph"]

class Graph(Collection[_Node], Generic[_Node, _NodeData, _EdgeData]):
    __networkx_backend__: ClassVar[str]
    node_dict_factory: ClassVar[_MapFactory]
    node_attr_dict_factory: ClassVar[_MapFactory]
    adjlist_outer_dict_factory: ClassVar[_MapFactory]
    adjlist_inner_dict_factory: ClassVar[_MapFactory]
    edge_attr_dict_factory: ClassVar[_MapFactory]
    graph_attr_dict_factory: ClassVar[_MapFactory]

    graph: dict[str, Any]
    __networkx_cache__: dict[str, Any]

    def to_directed_class(self) -> type[DiGraph[_Node, _NodeData, _EdgeData]]: ...
    def to_undirected_class(self) -> type[Graph[_Node, _NodeData, _EdgeData]]: ...
    # @_dispatchable adds `backend` argument, but this decorated is unsupported constructor type here
    # and __init__() ignores this argument
    def __new__(cls, *args, backend=None, **kwargs) -> Self: ...
    def __init__(
        self, incoming_graph_data: _Data[_Node, _NodeData, _EdgeData] | None = None, **attr: Any
    ) -> None: ...  # attr: key=value pairs
    @cached_property
    def adj(self) -> AdjacencyView[_Node, _Node, _EdgeData]: ...
    # This object is a read-only dict-like structure
    @property
    def name(self) -> str:
        """
        String identifier of the graph.

        This graph attribute appears in the attribute dict G.graph
        keyed by the string `"name"`. as well as an attribute (technically
        a property) `G.name`. This is entirely user controlled.
        """
        ...
    @name.setter
    def name(self, s: str) -> None: ...
    def __iter__(self) -> Iterator[_Node]: ...
    def __contains__(self, n: object) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, n: _Node) -> AtlasView[_Node, str, Any]: ...
    def add_node(self, node_for_adding: _Node, **attr: Any) -> None: ...  # attr: Set or change node attributes using key=value
    def add_nodes_from(
        self, nodes_for_adding: Iterable[_NodePlus[_Node, _NodeData]], **attr: Any
    ) -> None: ...  # attr: key=value pairs
    def remove_node(self, n: _Node) -> None: ...
    def remove_nodes_from(self, nodes: Iterable[_Node]) -> None: ...
    @cached_property
    def nodes(self) -> NodeView[_Node, _NodeData, _EdgeData]: ...
    def number_of_nodes(self) -> int: ...
    def order(self) -> int: ...
    def has_node(self, n: _Node) -> bool: ...
    # Including subtypes' possible return types for LSP
    def add_edge(self, u_of_edge: _Node, v_of_edge: _Node, **attr: Any) -> Hashable | None:
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
    # attr: Edge data (or labels or objects) can be assigned using keyword arguments
    def add_edges_from(self, ebunch_to_add: Iterable[_EdgePlus[_Node, _EdgeData]], **attr: Any) -> None: ...
    # attr: Edge data (or labels or objects) can be assigned using keyword arguments
    def add_weighted_edges_from(
        self, ebunch_to_add: Iterable[tuple[_Node, _Node, float | Decimal | None]], weight: str = "weight", **attr: Any
    ) -> None:
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
    # attr: Edge attributes to add/update for all edges.
    def remove_edge(self, u: _Node, v: _Node) -> None: ...
    def remove_edges_from(self, ebunch: Iterable[_EdgePlus[_Node, _EdgeData]]) -> None: ...
    @overload
    def update(self, edges: Graph[_Node, _NodeData, _EdgeData], nodes: None = None) -> None: ...
    @overload
    def update(
        self,
        edges: Graph[_Node, _NodeData, _EdgeData] | Iterable[_EdgePlus[_Node, _EdgeData]] | None = None,
        nodes: Iterable[_Node] | None = None,
    ) -> None: ...
    def has_edge(self, u: _Node, v: _Node) -> bool: ...
    def neighbors(self, n: _Node) -> Iterator[_Node]: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def edges(self) -> EdgeView[_Node, _NodeData, _EdgeData] | OutEdgeView[_Node, _NodeData, _EdgeData]: ...
    def get_edge_data(self, u: _Node, v: _Node, default: Any = None) -> _EdgeData: ...
    # default:  any Python object
    def adjacency(self) -> Iterator[tuple[_Node, dict[_Node, _EdgeData]]]: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def degree(self) -> DegreeView[_Node, _NodeData, _EdgeData] | DiDegreeView[_Node, _NodeData, _EdgeData]: ...
    def clear(self) -> None: ...
    def clear_edges(self) -> None: ...
    def is_multigraph(self) -> bool: ...
    def is_directed(self) -> bool: ...
    def copy(self, as_view: bool = False) -> Self: ...
    def to_directed(self, as_view: bool = False) -> DiGraph[_Node, _NodeData, _EdgeData]: ...
    def to_undirected(self, as_view: bool = False) -> Graph[_Node, _NodeData, _EdgeData]: ...
    def subgraph(self, nodes: _NBunch[_Node]) -> Self: ...
    def edge_subgraph(self, edges: Iterable[_Edge[_Node]]) -> Self: ...
    @overload
    def size(self, weight: None = None) -> int:
        """
        Returns the number of edges or total of all edge weights.

        Parameters
        ----------
        weight : string or None, optional (default=None)
            The edge attribute that holds the numerical value used
            as a weight. If None, then each edge has weight 1.

        Returns
        -------
        size : numeric
            The number of edges or
            (if weight keyword is provided) the total weight sum.

            If weight is None, returns an int. Otherwise a float
            (or more general numeric if the weights are more general).

        See Also
        --------
        number_of_edges

        Examples
        --------
        >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.size()
        3

        >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_edge("a", "b", weight=2)
        >>> G.add_edge("b", "c", weight=4)
        >>> G.size()
        2
        >>> G.size(weight="weight")
        6.0
        """
        ...
    @overload
    def size(self, weight: str) -> float:
        """
        Returns the number of edges or total of all edge weights.

        Parameters
        ----------
        weight : string or None, optional (default=None)
            The edge attribute that holds the numerical value used
            as a weight. If None, then each edge has weight 1.

        Returns
        -------
        size : numeric
            The number of edges or
            (if weight keyword is provided) the total weight sum.

            If weight is None, returns an int. Otherwise a float
            (or more general numeric if the weights are more general).

        See Also
        --------
        number_of_edges

        Examples
        --------
        >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.size()
        3

        >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_edge("a", "b", weight=2)
        >>> G.add_edge("b", "c", weight=4)
        >>> G.size()
        2
        >>> G.size(weight="weight")
        6.0
        """
        ...
    def number_of_edges(self, u: _Node | None = None, v: _Node | None = None) -> int:
        """
        Returns the number of edges between two nodes.

        Parameters
        ----------
        u, v : nodes, optional (default=all edges)
            If u and v are specified, return the number of edges between
            u and v. Otherwise return the total number of all edges.

        Returns
        -------
        nedges : int
            The number of edges in the graph.  If nodes `u` and `v` are
            specified return the number of edges between those nodes. If
            the graph is directed, this only returns the number of edges
            from `u` to `v`.

        See Also
        --------
        size

        Examples
        --------
        For undirected graphs, this method counts the total number of
        edges in the graph:

        >>> G = nx.path_graph(4)
        >>> G.number_of_edges()
        3

        If you specify two nodes, this counts the total number of edges
        joining the two nodes:

        >>> G.number_of_edges(0, 1)
        1

        For directed graphs, this method can count the total number of
        directed edges from `u` to `v`:

        >>> G = nx.DiGraph()
        >>> G.add_edge(0, 1)
        >>> G.add_edge(1, 0)
        >>> G.number_of_edges(0, 1)
        1
        """
        ...
    def nbunch_iter(self, nbunch: _NBunch[_Node] = None) -> Iterator[_Node]:
        """
        Returns an iterator over nodes contained in nbunch that are
        also in the graph.

        The nodes in an iterable nbunch are checked for membership in the graph
        and if not are silently ignored.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        Returns
        -------
        niter : iterator
            An iterator over nodes in nbunch that are also in the graph.
            If nbunch is None, iterate over all nodes in the graph.

        Raises
        ------
        NetworkXError
            If nbunch is not a node or sequence of nodes.
            If a node in nbunch is not hashable.

        See Also
        --------
        Graph.__iter__

        Notes
        -----
        When nbunch is an iterator, the returned iterator yields values
        directly from nbunch, becoming exhausted when nbunch is exhausted.

        To test whether nbunch is a single node, one can use
        "if nbunch in self:", even after processing with this routine.

        If nbunch is not a node or a (possibly empty) sequence/iterator
        or None, a :exc:`NetworkXError` is raised.  Also, if any object in
        nbunch is not hashable, a :exc:`NetworkXError` is raised.
        """
        ...
