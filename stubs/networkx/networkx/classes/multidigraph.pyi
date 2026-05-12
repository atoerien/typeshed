"""Base class for MultiDiGraph."""

from functools import cached_property
from typing import Any

from networkx.classes.coreviews import MultiAdjacencyView
from networkx.classes.digraph import DiGraph
from networkx.classes.graph import _EdgeData, _Node, _NodeData
from networkx.classes.multigraph import MultiGraph
from networkx.classes.reportviews import (
    DiMultiDegreeView,
    InMultiDegreeView,
    InMultiEdgeView,
    OutMultiDegreeView,
    OutMultiEdgeView,
)

__all__ = ["MultiDiGraph"]

# NOTE: Graph subclasses relationships are so complex
# we're only overriding methods that differ in signature from the base classes
# to use inheritance to our advantage and reduce complexity
class MultiDiGraph(MultiGraph[_Node, _NodeData, _EdgeData], DiGraph[_Node, _NodeData, _EdgeData]):
    @cached_property
    def succ(self) -> MultiAdjacencyView[_Node, _Node, dict[str, Any]]:
        """
        Graph adjacency object holding the successors of each node.

        This object is a read-only dict-like structure with node keys
        and neighbor-dict values.  The neighbor-dict is keyed by neighbor
        to the edgekey-dict.  So `G.adj[3][2][0]['color'] = 'blue'` sets
        the color of the edge `(3, 2, 0)` to `"blue"`.

        Iterating over G.adj behaves like a dict. Useful idioms include
        `for nbr, datadict in G.adj[n].items():`.

        The neighbor information is also provided by subscripting the graph.
        So `for nbr, foovalue in G[node].data('foo', default=1):` works.

        For directed graphs, `G.succ` is identical to `G.adj`.
        """
        ...
    @cached_property
    def pred(self) -> MultiAdjacencyView[_Node, _Node, dict[str, Any]]:
        """
        Graph adjacency object holding the predecessors of each node.

        This object is a read-only dict-like structure with node keys
        and neighbor-dict values.  The neighbor-dict is keyed by neighbor
        to the edgekey-dict.  So `G.adj[3][2][0]['color'] = 'blue'` sets
        the color of the edge `(3, 2, 0)` to `"blue"`.

        Iterating over G.adj behaves like a dict. Useful idioms include
        `for nbr, datadict in G.adj[n].items():`.
        """
        ...
    @cached_property
    def edges(self) -> OutMultiEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def out_edges(self) -> OutMultiEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def in_edges(self) -> InMultiEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def degree(self) -> DiMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def in_degree(self) -> InMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def out_degree(self) -> OutMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    def to_undirected(self, reciprocal: bool = False, as_view: bool = False) -> MultiGraph[_Node, _NodeData, _EdgeData]: ...  # type: ignore[override] # Has an additional `reciprocal` keyword argument
