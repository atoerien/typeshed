"""Base class for directed graphs."""

from collections.abc import Iterator
from functools import cached_property
from typing import Any
from typing_extensions import Self

from networkx.classes.coreviews import AdjacencyView
from networkx.classes.graph import Graph, _EdgeData, _Node, _NodeData
from networkx.classes.reportviews import (
    DiDegreeView,
    InDegreeView,
    InEdgeView,
    InMultiDegreeView,
    InMultiEdgeView,
    OutDegreeView,
    OutEdgeView,
    OutMultiDegreeView,
)

__all__ = ["DiGraph"]

# NOTE: Graph subclasses relationships are so complex
# we're only overriding methods that differ in signature from the base classes
# to use inheritance to our advantage and reduce complexity
class DiGraph(Graph[_Node, _NodeData, _EdgeData]):
    @cached_property
    def succ(self) -> AdjacencyView[_Node, _Node, dict[str, Any]]:
        """
        Graph adjacency object holding the successors of each node.

        This object is a read-only dict-like structure with node keys
        and neighbor-dict values.  The neighbor-dict is keyed by neighbor
        to the edge-data-dict.  So `G.succ[3][2]['color'] = 'blue'` sets
        the color of the edge `(3, 2)` to `"blue"`.

        Iterating over G.succ behaves like a dict. Useful idioms include
        `for nbr, datadict in G.succ[n].items():`.  A data-view not provided
        by dicts also exists: `for nbr, foovalue in G.succ[node].data('foo'):`
        and a default can be set via a `default` argument to the `data` method.

        The neighbor information is also provided by subscripting the graph.
        So `for nbr, foovalue in G[node].data('foo', default=1):` works.

        For directed graphs, `G.adj` is identical to `G.succ`.
        """
        ...
    @cached_property
    def pred(self) -> AdjacencyView[_Node, _Node, dict[str, Any]]:
        """
        Graph adjacency object holding the predecessors of each node.

        This object is a read-only dict-like structure with node keys
        and neighbor-dict values.  The neighbor-dict is keyed by neighbor
        to the edge-data-dict.  So `G.pred[2][3]['color'] = 'blue'` sets
        the color of the edge `(3, 2)` to `"blue"`.

        Iterating over G.pred behaves like a dict. Useful idioms include
        `for nbr, datadict in G.pred[n].items():`.  A data-view not provided
        by dicts also exists: `for nbr, foovalue in G.pred[node].data('foo'):`
        A default can be set via a `default` argument to the `data` method.
        """
        ...
    def has_successor(self, u: _Node, v: _Node) -> bool:
        """
        Returns True if node u has successor v.

        This is true if graph has the edge u->v.
        """
        ...
    def has_predecessor(self, u: _Node, v: _Node) -> bool:
        """
        Returns True if node u has predecessor v.

        This is true if graph has the edge u<-v.
        """
        ...
    def successors(self, n: _Node) -> Iterator[_Node]:
        """
        Returns an iterator over successor nodes of n.

        A successor of n is a node m such that there exists a directed
        edge from n to m.

        Parameters
        ----------
        n : node
           A node in the graph

        Raises
        ------
        NetworkXError
           If n is not in the graph.

        See Also
        --------
        predecessors

        Notes
        -----
        neighbors() and successors() are the same.
        """
        ...

    neighbors = successors

    def predecessors(self, n: _Node) -> Iterator[_Node]:
        """
        Returns an iterator over predecessor nodes of n.

        A predecessor of n is a node m such that there exists a directed
        edge from m to n.

        Parameters
        ----------
        n : node
           A node in the graph

        Raises
        ------
        NetworkXError
           If n is not in the graph.

        See Also
        --------
        successors
        """
        ...
    @cached_property
    def edges(self) -> OutEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def out_edges(self) -> OutEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def in_edges(self) -> InEdgeView[_Node, _NodeData, _EdgeData] | InMultiEdgeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    def degree(self) -> DiDegreeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def in_degree(self) -> InDegreeView[_Node, _NodeData, _EdgeData] | InMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    @cached_property
    # Including subtypes' possible return types for LSP
    def out_degree(self) -> OutDegreeView[_Node, _NodeData, _EdgeData] | OutMultiDegreeView[_Node, _NodeData, _EdgeData]: ...
    def to_undirected(self, reciprocal: bool = False, as_view: bool = False) -> Graph[_Node, _NodeData, _EdgeData]: ...  # type: ignore[override] # Has an additional `reciprocal` keyword argument
    def reverse(self, copy: bool = True) -> Self: ...
