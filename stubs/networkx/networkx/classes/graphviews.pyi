"""
View of Graphs as SubGraph, Reverse, Directed, Undirected.

In some algorithms it is convenient to temporarily morph
a graph to exclude some nodes or edges. It should be better
to do that via a view than to remove and then re-add.
In other algorithms it is convenient to temporarily morph
a graph to reverse directed edges, or treat a directed graph
as undirected, etc. This module provides those graph views.

The resulting views are essentially read-only graphs that
report data from the original graph object. We provide an
attribute G._graph which points to the underlying graph object.

Note: Since graphviews look like graphs, one can end up with
view-of-view-of-view chains. Be careful with chains because
they become very slow with about 15 nested views.
For the common simple case of node induced subgraphs created
from the graph class, we short-cut the chain by returning a
subgraph of the original graph directly rather than a subgraph
of a subgraph. We are careful not to disrupt any edge filter in
the middle subgraph. In general, determining how to short-cut
the chain is tricky and much harder with restricted_views than
with induced subgraphs.
Often it is easiest to use .copy() to avoid chains.
"""

from collections.abc import Callable, Hashable
from typing import TypeVar, overload

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph, _DataBound, _EdgeData, _Node, _NodeData
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph

_G = TypeVar("_G", bound=Graph[Hashable, _DataBound, _DataBound])
_D = TypeVar("_D", bound=DiGraph[Hashable, _DataBound, _DataBound])

__all__ = ["generic_graph_view", "subgraph_view", "reverse_view"]

@overload
def generic_graph_view(G: _G, create_using: None = None) -> _G:
    """
    Returns a read-only view of `G`.

    The graph `G` and its attributes are not copied but viewed through the new graph object
    of the same class as `G` (or of the class specified in `create_using`).

    Parameters
    ----------
    G : graph
        A directed/undirected graph/multigraph.

    create_using : NetworkX graph constructor, optional (default=None)
       Graph type to create. If graph instance, then cleared before populated.
       If `None`, then the appropriate Graph type is inferred from `G`.

    Returns
    -------
    newG : graph
        A view of the input graph `G` and its attributes as viewed through
        the `create_using` class.

    Raises
    ------
    NetworkXError
        If `G` is a multigraph (or multidigraph) but `create_using` is not, or vice versa.

    Notes
    -----
    The returned graph view is read-only (cannot modify the graph).
    Yet the view reflects any changes in `G`. The intent is to mimic dict views.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_edge(1, 2, weight=0.3)
    >>> G.add_edge(2, 3, weight=0.5)
    >>> G.edges(data=True)
    EdgeDataView([(1, 2, {'weight': 0.3}), (2, 3, {'weight': 0.5})])

    The view exposes the attributes from the original graph.

    >>> viewG = nx.graphviews.generic_graph_view(G)
    >>> viewG.edges(data=True)
    EdgeDataView([(1, 2, {'weight': 0.3}), (2, 3, {'weight': 0.5})])

    Changes to `G` are reflected in `viewG`.

    >>> G.remove_edge(2, 3)
    >>> G.edges(data=True)
    EdgeDataView([(1, 2, {'weight': 0.3})])

    >>> viewG.edges(data=True)
    EdgeDataView([(1, 2, {'weight': 0.3})])

    We can change the graph type with the `create_using` parameter.

    >>> type(G)
    <class 'networkx.classes.graph.Graph'>
    >>> viewDG = nx.graphviews.generic_graph_view(G, create_using=nx.DiGraph)
    >>> type(viewDG)
    <class 'networkx.classes.digraph.DiGraph'>
    """
    ...
@overload
def generic_graph_view(
    G: Graph[_Node, _NodeData, _EdgeData], create_using: type[MultiDiGraph[_Node, _NodeData, _EdgeData]]
) -> MultiDiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def generic_graph_view(
    G: Graph[_Node, _NodeData, _EdgeData], create_using: type[DiGraph[_Node, _NodeData, _EdgeData]]
) -> DiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def generic_graph_view(
    G: Graph[_Node, _NodeData, _EdgeData], create_using: type[MultiGraph[_Node, _NodeData, _EdgeData]]
) -> MultiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def generic_graph_view(
    G: Graph[_Node, _NodeData, _EdgeData], create_using: type[Graph[_Node, _NodeData, _EdgeData]]
) -> Graph[_Node, _NodeData, _EdgeData]: ...
@overload
def subgraph_view(
    G: MultiDiGraph[_Node, _NodeData, _EdgeData],
    *,
    filter_node: Callable[[_Node], bool] = ...,
    filter_edge: Callable[[_Node, _Node, int], bool] = ...,
) -> MultiDiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def subgraph_view(
    G: MultiGraph[_Node, _NodeData, _EdgeData],
    *,
    filter_node: Callable[[_Node], bool] = ...,
    filter_edge: Callable[[_Node, _Node, int], bool] = ...,
) -> MultiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def subgraph_view(
    G: DiGraph[_Node, _NodeData, _EdgeData],
    *,
    filter_node: Callable[[_Node], bool] = ...,
    filter_edge: Callable[[_Node, _Node], bool] = ...,
) -> DiGraph[_Node, _NodeData, _EdgeData]: ...
@overload
def subgraph_view(
    G: Graph[_Node, _NodeData, _EdgeData],
    *,
    filter_node: Callable[[_Node], bool] = ...,
    filter_edge: Callable[[_Node, _Node], bool] = ...,
) -> Graph[_Node, _NodeData, _EdgeData]: ...
def reverse_view(G: _D) -> _D: ...
