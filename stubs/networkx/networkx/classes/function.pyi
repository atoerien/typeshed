"""Functional interface to graph methods and assorted utilities."""

from _typeshed import Incomplete, SupportsItems, SupportsKeysAndGetItem, Unused
from collections.abc import Callable, Generator, Hashable, Iterable, Iterator
from typing import Literal, TypeVar, overload

from networkx import _dispatchable
from networkx.algorithms.planarity import PlanarEmbedding
from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _EdgeData, _NBunch, _Node, _NodeData
from networkx.classes.multigraph import MultiGraph

__all__ = [
    "nodes",
    "edges",
    "degree",
    "degree_histogram",
    "neighbors",
    "number_of_nodes",
    "number_of_edges",
    "density",
    "is_directed",
    "freeze",
    "is_frozen",
    "subgraph",
    "induced_subgraph",
    "edge_subgraph",
    "restricted_view",
    "to_directed",
    "to_undirected",
    "add_star",
    "add_path",
    "add_cycle",
    "create_empty_copy",
    "set_node_attributes",
    "get_node_attributes",
    "remove_node_attributes",
    "set_edge_attributes",
    "get_edge_attributes",
    "remove_edge_attributes",
    "all_neighbors",
    "non_neighbors",
    "non_edges",
    "common_neighbors",
    "is_weighted",
    "is_negatively_weighted",
    "is_empty",
    "selfloop_edges",
    "nodes_with_selfloops",
    "number_of_selfloops",
    "path_weight",
    "is_path",
    "describe",
]

_U = TypeVar("_U")

def nodes(G: Graph[_Node]): ...
def edges(G: Graph[_Node], nbunch=None): ...
def degree(G: Graph[_Node], nbunch=None, weight=None): ...
def neighbors(G: Graph[_Node], n): ...
def number_of_nodes(G: Graph[_Node]): ...
def number_of_edges(G: Graph[_Node]): ...
def density(G: Graph[_Node]): ...
def degree_histogram(G: Graph[_Node]) -> list[int]: ...

@overload
def is_directed(G: PlanarEmbedding[Hashable]) -> Literal[False]:
    """Return True if graph is directed."""
    ...
@overload
def is_directed(G: DiGraph[Hashable]) -> Literal[True]:
    """Return True if graph is directed."""
    ...
@overload
def is_directed(G: Graph[Hashable]) -> Literal[False]: ...

def freeze(G: Graph[_Node]): ...
def is_frozen(G: Graph[Incomplete]) -> bool: ...
def add_star(G_to_add_to, nodes_for_star, **attr) -> None: ...
def add_path(G_to_add_to, nodes_for_path, **attr) -> None: ...
def add_cycle(G_to_add_to, nodes_for_cycle, **attr) -> None: ...
def subgraph(G: Graph[_Node], nbunch): ...
def induced_subgraph(G: Graph[_Node, _NodeData, _EdgeData], nbunch: _NBunch[_Node]) -> Graph[_Node, _NodeData, _EdgeData]: ...
def edge_subgraph(G: Graph[_Node], edges): ...
def restricted_view(G: Graph[_Node], nodes, edges): ...
def to_directed(graph): ...
def to_undirected(graph): ...
def create_empty_copy(G: Graph[_Node], with_data: bool = True): ...

# incomplete: Can "Any scalar value" be enforced?
@overload
def set_node_attributes(
    G: Graph[Hashable],
    values: SupportsItems[_Node, Unused],
    name: str,
    *,
    backend=None,  # @_dispatchable adds these arguments, but we can't use this decorator with @overload
    **backend_kwargs,
) -> None:
    """
    Sets node attributes from a given value or dictionary of values.

    .. Warning:: The call order of arguments `values` and `name`
        switched between v1.x & v2.x.

    Parameters
    ----------
    G : NetworkX Graph

    values : scalar value, dict-like
        What the node attribute should be set to.  If `values` is
        not a dictionary, then it is treated as a single attribute value
        that is then applied to every node in `G`.  This means that if
        you provide a mutable object, like a list, updates to that object
        will be reflected in the node attribute for every node.
        The attribute name will be `name`.

        If `values` is a dict or a dict of dict, it should be keyed
        by node to either an attribute value or a dict of attribute key/value
        pairs used to update the node's attributes.

    name : string (optional, default=None)
        Name of the node attribute to set if values is a scalar.

    Examples
    --------
    After computing some property of the nodes of a graph, you may want
    to assign a node attribute to store the value of that property for
    each node::

        >>> G = nx.path_graph(3)
        >>> bb = nx.betweenness_centrality(G)
        >>> isinstance(bb, dict)
        True
        >>> nx.set_node_attributes(G, bb, "betweenness")
        >>> G.nodes[1]["betweenness"]
        1.0

    If you provide a list as the second argument, updates to the list
    will be reflected in the node attribute for each node::

        >>> G = nx.path_graph(3)
        >>> labels = []
        >>> nx.set_node_attributes(G, labels, "labels")
        >>> labels.append("foo")
        >>> G.nodes[0]["labels"]
        ['foo']
        >>> G.nodes[1]["labels"]
        ['foo']
        >>> G.nodes[2]["labels"]
        ['foo']

    If you provide a dictionary of dictionaries as the second argument,
    the outer dictionary is assumed to be keyed by node to an inner
    dictionary of node attributes for that node::

        >>> G = nx.path_graph(3)
        >>> attrs = {0: {"attr1": 20, "attr2": "nothing"}, 1: {"attr2": 3}}
        >>> nx.set_node_attributes(G, attrs)
        >>> G.nodes[0]["attr1"]
        20
        >>> G.nodes[0]["attr2"]
        'nothing'
        >>> G.nodes[1]["attr2"]
        3
        >>> G.nodes[2]
        {}

    Note that if the dictionary contains nodes that are not in `G`, the
    values are silently ignored::

        >>> G = nx.Graph()
        >>> G.add_node(0)
        >>> nx.set_node_attributes(G, {0: "red", 1: "blue"}, name="color")
        >>> G.nodes[0]["color"]
        'red'
        >>> 1 in G.nodes
        False
    """
    ...
@overload
def set_node_attributes(
    G: Graph[_Node],
    values: SupportsItems[_Node, SupportsKeysAndGetItem[Incomplete, Incomplete] | Iterable[tuple[Incomplete, Incomplete]]],
    name: None = None,
    *,
    backend=None,
    **backend_kwargs,
) -> None: ...

@_dispatchable
def get_node_attributes(G: Graph[_Node], name: str, default=None) -> dict[_Node, Incomplete]:
    """
    Get node attributes from graph

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    default: object (default=None)
       Default value of the node attribute if there is no value set for that
       node in graph. If `None` then nodes without this attribute are not
       included in the returned dict.

    Returns
    -------
    Dictionary of attributes keyed by node.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_nodes_from([1, 2, 3], color="red")
    >>> color = nx.get_node_attributes(G, "color")
    >>> color[1]
    'red'
    >>> G.add_node(4)
    >>> color = nx.get_node_attributes(G, "color", default="yellow")
    >>> color[4]
    'yellow'
    """
    ...
@_dispatchable
def remove_node_attributes(G: Graph[_Node], *attr_names, nbunch=None) -> None: ...

@overload
def set_edge_attributes(
    G: Graph[_Node],
    values: SupportsItems[tuple[_Node, _Node], Incomplete],
    name: str,
    *,
    backend: str | None = None,  # @_dispatchable adds these arguments, but we can't use this decorator with @overload
    **backend_kwargs,
) -> None:
    """
    Sets edge attributes from a given value or dictionary of values.

    .. Warning:: The call order of arguments `values` and `name`
        switched between v1.x & v2.x.

    Parameters
    ----------
    G : NetworkX Graph

    values : scalar value, dict-like
        What the edge attribute should be set to.  If `values` is
        not a dictionary, then it is treated as a single attribute value
        that is then applied to every edge in `G`.  This means that if
        you provide a mutable object, like a list, updates to that object
        will be reflected in the edge attribute for each edge.  The attribute
        name will be `name`.

        If `values` is a dict or a dict of dict, it should be keyed
        by edge tuple to either an attribute value or a dict of attribute
        key/value pairs used to update the edge's attributes.
        For multigraphs, the edge tuples must be of the form ``(u, v, key)``,
        where `u` and `v` are nodes and `key` is the edge key.
        For non-multigraphs, the keys must be tuples of the form ``(u, v)``.

    name : string (optional, default=None)
        Name of the edge attribute to set if values is a scalar.

    Examples
    --------
    After computing some property of the edges of a graph, you may want
    to assign a edge attribute to store the value of that property for
    each edge::

        >>> G = nx.path_graph(3)
        >>> bb = nx.edge_betweenness_centrality(G, normalized=False)
        >>> nx.set_edge_attributes(G, bb, "betweenness")
        >>> G.edges[1, 2]["betweenness"]
        2.0

    If you provide a list as the second argument, updates to the list
    will be reflected in the edge attribute for each edge::

        >>> labels = []
        >>> nx.set_edge_attributes(G, labels, "labels")
        >>> labels.append("foo")
        >>> G.edges[0, 1]["labels"]
        ['foo']
        >>> G.edges[1, 2]["labels"]
        ['foo']

    If you provide a dictionary of dictionaries as the second argument,
    the entire dictionary will be used to update edge attributes::

        >>> G = nx.path_graph(3)
        >>> attrs = {(0, 1): {"attr1": 20, "attr2": "nothing"}, (1, 2): {"attr2": 3}}
        >>> nx.set_edge_attributes(G, attrs)
        >>> G[0][1]["attr1"]
        20
        >>> G[0][1]["attr2"]
        'nothing'
        >>> G[1][2]["attr2"]
        3

    The attributes of one Graph can be used to set those of another.

        >>> H = nx.path_graph(3)
        >>> nx.set_edge_attributes(H, G.edges)

    Note that if the dict contains edges that are not in `G`, they are
    silently ignored::

        >>> G = nx.Graph([(0, 1)])
        >>> nx.set_edge_attributes(G, {(1, 2): {"weight": 2.0}})
        >>> (1, 2) in G.edges()
        False

    For multigraphs, the `values` dict is expected to be keyed by 3-tuples
    including the edge key::

        >>> MG = nx.MultiGraph()
        >>> edges = [(0, 1), (0, 1)]
        >>> MG.add_edges_from(edges)  # Returns list of edge keys
        [0, 1]
        >>> attributes = {(0, 1, 0): {"cost": 21}, (0, 1, 1): {"cost": 7}}
        >>> nx.set_edge_attributes(MG, attributes)
        >>> MG[0][1][0]["cost"]
        21
        >>> MG[0][1][1]["cost"]
        7

    If MultiGraph attributes are desired for a Graph, you must convert the 3-tuple
    multiedge to a 2-tuple edge and the last multiedge's attribute value will
    overwrite the previous values. Continuing from the previous case we get::

        >>> H = nx.path_graph([0, 1, 2])
        >>> nx.set_edge_attributes(H, {(u, v): ed for u, v, ed in MG.edges.data()})
        >>> nx.get_edge_attributes(H, "cost")
        {(0, 1): 7}
    """
    ...
@overload
def set_edge_attributes(
    G: MultiGraph[_Node],
    values: dict[tuple[_Node, _Node, Incomplete], Incomplete],
    name: str,
    *,
    backend: str | None = None,
    **backend_kwargs,
) -> None:
    """
    Sets edge attributes from a given value or dictionary of values.

    .. Warning:: The call order of arguments `values` and `name`
        switched between v1.x & v2.x.

    Parameters
    ----------
    G : NetworkX Graph

    values : scalar value, dict-like
        What the edge attribute should be set to.  If `values` is
        not a dictionary, then it is treated as a single attribute value
        that is then applied to every edge in `G`.  This means that if
        you provide a mutable object, like a list, updates to that object
        will be reflected in the edge attribute for each edge.  The attribute
        name will be `name`.

        If `values` is a dict or a dict of dict, it should be keyed
        by edge tuple to either an attribute value or a dict of attribute
        key/value pairs used to update the edge's attributes.
        For multigraphs, the edge tuples must be of the form ``(u, v, key)``,
        where `u` and `v` are nodes and `key` is the edge key.
        For non-multigraphs, the keys must be tuples of the form ``(u, v)``.

    name : string (optional, default=None)
        Name of the edge attribute to set if values is a scalar.

    Examples
    --------
    After computing some property of the edges of a graph, you may want
    to assign a edge attribute to store the value of that property for
    each edge::

        >>> G = nx.path_graph(3)
        >>> bb = nx.edge_betweenness_centrality(G, normalized=False)
        >>> nx.set_edge_attributes(G, bb, "betweenness")
        >>> G.edges[1, 2]["betweenness"]
        2.0

    If you provide a list as the second argument, updates to the list
    will be reflected in the edge attribute for each edge::

        >>> labels = []
        >>> nx.set_edge_attributes(G, labels, "labels")
        >>> labels.append("foo")
        >>> G.edges[0, 1]["labels"]
        ['foo']
        >>> G.edges[1, 2]["labels"]
        ['foo']

    If you provide a dictionary of dictionaries as the second argument,
    the entire dictionary will be used to update edge attributes::

        >>> G = nx.path_graph(3)
        >>> attrs = {(0, 1): {"attr1": 20, "attr2": "nothing"}, (1, 2): {"attr2": 3}}
        >>> nx.set_edge_attributes(G, attrs)
        >>> G[0][1]["attr1"]
        20
        >>> G[0][1]["attr2"]
        'nothing'
        >>> G[1][2]["attr2"]
        3

    The attributes of one Graph can be used to set those of another.

        >>> H = nx.path_graph(3)
        >>> nx.set_edge_attributes(H, G.edges)

    Note that if the dict contains edges that are not in `G`, they are
    silently ignored::

        >>> G = nx.Graph([(0, 1)])
        >>> nx.set_edge_attributes(G, {(1, 2): {"weight": 2.0}})
        >>> (1, 2) in G.edges()
        False

    For multigraphs, the `values` dict is expected to be keyed by 3-tuples
    including the edge key::

        >>> MG = nx.MultiGraph()
        >>> edges = [(0, 1), (0, 1)]
        >>> MG.add_edges_from(edges)  # Returns list of edge keys
        [0, 1]
        >>> attributes = {(0, 1, 0): {"cost": 21}, (0, 1, 1): {"cost": 7}}
        >>> nx.set_edge_attributes(MG, attributes)
        >>> MG[0][1][0]["cost"]
        21
        >>> MG[0][1][1]["cost"]
        7

    If MultiGraph attributes are desired for a Graph, you must convert the 3-tuple
    multiedge to a 2-tuple edge and the last multiedge's attribute value will
    overwrite the previous values. Continuing from the previous case we get::

        >>> H = nx.path_graph([0, 1, 2])
        >>> nx.set_edge_attributes(H, {(u, v): ed for u, v, ed in MG.edges.data()})
        >>> nx.get_edge_attributes(H, "cost")
        {(0, 1): 7}
    """
    ...
@overload
def set_edge_attributes(
    G: Graph[Hashable], values, name: None = None, *, backend: str | None = None, **backend_kwargs
) -> None: ...

@_dispatchable
def get_edge_attributes(G: Graph[_Node], name: str, default=None) -> dict[tuple[_Node, _Node], Incomplete]:
    """
    Get edge attributes from graph

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    default: object (default=None)
       Default value of the edge attribute if there is no value set for that
       edge in graph. If `None` then edges without this attribute are not
       included in the returned dict.

    Returns
    -------
    Dictionary of attributes keyed by edge. For (di)graphs, the keys are
    2-tuples of the form: (u, v). For multi(di)graphs, the keys are 3-tuples of
    the form: (u, v, key).

    Examples
    --------
    >>> G = nx.Graph()
    >>> nx.add_path(G, [1, 2, 3], color="red")
    >>> color = nx.get_edge_attributes(G, "color")
    >>> color[(1, 2)]
    'red'
    >>> G.add_edge(3, 4)
    >>> color = nx.get_edge_attributes(G, "color", default="yellow")
    >>> color[(3, 4)]
    'yellow'
    """
    ...
@_dispatchable
def remove_edge_attributes(G: Graph[_Node], *attr_names, ebunch=None) -> None:
    """
    Remove edge attributes from all edges in the graph.

    Parameters
    ----------
    G : NetworkX Graph

    *attr_names : List of Strings
        The attribute names to remove from the graph.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> nx.set_edge_attributes(G, {(u, v): u + v for u, v in G.edges()}, name="weight")
    >>> nx.get_edge_attributes(G, "weight")
    {(0, 1): 1, (1, 2): 3}
    >>> remove_edge_attributes(G, "weight")
    >>> nx.get_edge_attributes(G, "weight")
    {}
    """
    ...
def all_neighbors(graph: Graph[_Node], node: _Node) -> Iterator[_Node]:
    """
    Returns all of the neighbors of a node in the graph.

    If the graph is directed returns predecessors as well as successors.

    Parameters
    ----------
    graph : NetworkX graph
        Graph to find neighbors.
    node : node
        The node whose neighbors will be returned.

    Returns
    -------
    neighbors : iterator
        Iterator of neighbors

    Raises
    ------
    NetworkXError
        If `node` is not in the graph.

    Examples
    --------
    For undirected graphs, this function is equivalent to ``G.neighbors(node)``.

    >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
    >>> list(nx.all_neighbors(G, 1))
    [0, 2]

    For directed graphs, this function returns both predecessors and successors,
    which may include duplicates if a node is both a predecessor and successor
    (e.g., in bidirectional edges or self-loops).

    >>> DG = nx.DiGraph([(0, 1), (1, 2), (2, 1)])
    >>> list(nx.all_neighbors(DG, 1))
    [0, 2, 2]

    Notes
    -----
    This function iterates over all neighbors (both predecessors and successors).

    See Also
    --------
    Graph.neighbors : Returns successors for both Graph and DiGraph
    DiGraph.predecessors : Returns predecessors for directed graphs only
    DiGraph.successors : Returns successors for directed graphs only
    """
    ...
def non_neighbors(graph: Graph[_Node], node: _Node) -> Generator[_Node]:
    """
    Returns the non-neighbors of the node in the graph.

    Parameters
    ----------
    graph : NetworkX graph
        Graph to find neighbors.

    node : node
        The node whose neighbors will be returned.

    Returns
    -------
    non_neighbors : set
        Set of nodes in the graph that are not neighbors of the node.
    """
    ...
def non_edges(graph: Graph[_Node]) -> Generator[tuple[_Node, _Node]]:
    """
    Returns the nonexistent edges in the graph.

    Parameters
    ----------
    graph : NetworkX graph.
        Graph to find nonexistent edges.

    Returns
    -------
    non_edges : iterator
        Iterator of edges that are not in the graph.
    """
    ...
def common_neighbors(G: Graph[_Node], u: _Node, v: _Node) -> Generator[_Node]:
    """
    Returns the common neighbors of two nodes in a graph.

    Parameters
    ----------
    G : graph
        A NetworkX undirected graph.

    u, v : nodes
        Nodes in the graph.

    Returns
    -------
    cnbors : set
        Set of common neighbors of u and v in the graph.

    Raises
    ------
    NetworkXError
        If u or v is not a node in the graph.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> sorted(nx.common_neighbors(G, 0, 1))
    [2, 3, 4]
    """
    ...
@_dispatchable
def is_weighted(G: Graph[_Node], edge: tuple[_Node, _Node] | None = None, weight: str = "weight") -> bool:
    """
    Returns True if `G` has weighted edges.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    edge : tuple, optional
        A 2-tuple specifying the only edge in `G` that will be tested. If
        None, then every edge in `G` is tested.

    weight: string, optional
        The attribute name used to query for edge weights.

    Returns
    -------
    bool
        A boolean signifying if `G`, or the specified edge, is weighted.

    Raises
    ------
    NetworkXError
        If the specified edge does not exist.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.is_weighted(G)
    False
    >>> nx.is_weighted(G, (2, 3))
    False

    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2, weight=1)
    >>> nx.is_weighted(G)
    True
    """
    ...
@_dispatchable
def is_negatively_weighted(G: Graph[_Node], edge: tuple[_Node, _Node] | None = None, weight: str = "weight") -> bool:
    """
    Returns True if `G` has negatively weighted edges.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    edge : tuple, optional
        A 2-tuple specifying the only edge in `G` that will be tested. If
        None, then every edge in `G` is tested.

    weight: string, optional
        The attribute name used to query for edge weights.

    Returns
    -------
    bool
        A boolean signifying if `G`, or the specified edge, is negatively
        weighted.

    Raises
    ------
    NetworkXError
        If the specified edge does not exist.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_edges_from([(1, 3), (2, 4), (2, 6)])
    >>> G.add_edge(1, 2, weight=4)
    >>> nx.is_negatively_weighted(G, (1, 2))
    False
    >>> G[2][4]["weight"] = -2
    >>> nx.is_negatively_weighted(G)
    True
    >>> G = nx.DiGraph()
    >>> edges = [("0", "3", 3), ("0", "1", -5), ("1", "0", -2)]
    >>> G.add_weighted_edges_from(edges)
    >>> nx.is_negatively_weighted(G)
    True
    """
    ...
@_dispatchable
def is_empty(G: Graph[Hashable]) -> bool: ...
def nodes_with_selfloops(G: Graph[_Node]) -> Generator[_Node]: ...

@overload
def selfloop_edges(
    G: Graph[_Node], data: Literal[False] = False, keys: Literal[False] = False, default=None
) -> Generator[tuple[_Node, _Node]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node, _NodeData, _EdgeData], data: Literal[True], keys: Literal[False] = False, default=None
) -> Generator[tuple[_Node, _Node, _EdgeData]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node], data: str, keys: Literal[False] = False, default: _U | None = None
) -> Generator[tuple[_Node, _Node, _U]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node], data: Literal[False], keys: Literal[True], default=None
) -> Generator[tuple[_Node, _Node, int]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node], data: Literal[False] = False, *, keys: Literal[True], default=None
) -> Generator[tuple[_Node, _Node, int]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node, _NodeData, _EdgeData], data: Literal[True], keys: Literal[True], default=None
) -> Generator[tuple[_Node, _Node, int, _EdgeData]]:
    """
    Returns an iterator over selfloop edges.

    A selfloop edge has the same node at both ends.

    Parameters
    ----------
    G : graph
        A NetworkX graph.
    data : string or bool, optional (default=False)
        Return selfloop edges as two tuples (u, v) (data=False)
        or three-tuples (u, v, datadict) (data=True)
        or three-tuples (u, v, datavalue) (data='attrname')
    keys : bool, optional (default=False)
        If True, return edge keys with each edge.
    default : value, optional (default=None)
        Value used for edges that don't have the requested attribute.
        Only relevant if data is not True or False.

    Returns
    -------
    edgeiter : iterator over edge tuples
        An iterator over all selfloop edges.

    See Also
    --------
    nodes_with_selfloops, number_of_selfloops

    Examples
    --------
    >>> G = nx.MultiGraph()  # or Graph, DiGraph, MultiDiGraph, etc
    >>> ekey = G.add_edge(1, 1)
    >>> ekey = G.add_edge(1, 2)
    >>> list(nx.selfloop_edges(G))
    [(1, 1)]
    >>> list(nx.selfloop_edges(G, data=True))
    [(1, 1, {})]
    >>> list(nx.selfloop_edges(G, keys=True))
    [(1, 1, 0)]
    >>> list(nx.selfloop_edges(G, keys=True, data=True))
    [(1, 1, 0, {})]
    """
    ...
@overload
def selfloop_edges(
    G: Graph[_Node], data: str, keys: Literal[True], default: _U | None = None
) -> Generator[tuple[_Node, _Node, int, _U]]: ...

@_dispatchable
def number_of_selfloops(G: Graph[Hashable]) -> int:
    """
    Returns the number of selfloop edges.

    A selfloop edge has the same node at both ends.

    Returns
    -------
    nloops : int
        The number of selfloops.

    See Also
    --------
    nodes_with_selfloops, selfloop_edges

    Examples
    --------
    >>> G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
    >>> G.add_edge(1, 1)
    >>> G.add_edge(1, 2)
    >>> nx.number_of_selfloops(G)
    1
    """
    ...
def is_path(G: Graph[_Node], path: Iterable[Incomplete]) -> bool:
    """
    Returns whether or not the specified path exists.

    For it to return True, every node on the path must exist and
    each consecutive pair must be connected via one or more edges.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    path : list
        A list of nodes which defines the path to traverse

    Returns
    -------
    bool
        True if `path` is a valid path in `G`
    """
    ...
def path_weight(G: Graph[_Node], path, weight) -> int:
    """
    Returns total cost associated with specified path and weight

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    path: list
        A list of node labels which defines the path to traverse

    weight: string
        A string indicating which edge attribute to use for path cost

    Returns
    -------
    cost: int or float
        An integer or a float representing the total cost with respect to the
        specified weight of the specified path

    Raises
    ------
    NetworkXNoPath
        If the specified edge does not exist.
    """
    ...
def describe(G: Graph[_Node], describe_hook: Callable[[Graph[_Node]], dict[str, Incomplete]] | None = None) -> None:
    """
    Prints a description of the graph G.

    By default, the description includes some basic properties of the graph.
    You can also provide additional functions to compute and include
    more properties in the description.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    describe_hook: callable, optional (default=None)
        A function that takes a graph as input and returns a
        dictionary of additional properties to include in the description.
        The keys of the dictionary are the property names, and the values
        are the corresponding property values.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.describe(G)
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1

    >>> def augment_description(G):
    ...     return {"Average Shortest Path Length": nx.average_shortest_path_length(G)}
    >>> nx.describe(G, describe_hook=augment_description)
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1
    Average Shortest Path Length   : 2.0

    >>> G.name = "Path Graph of 5 nodes"
    >>> nx.describe(G)
    Name of Graph                  : Path Graph of 5 nodes
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1
    """
    ...
