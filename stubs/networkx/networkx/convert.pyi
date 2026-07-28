"""
Functions to convert NetworkX graphs to and from other formats.

The preferred way of converting data to a NetworkX graph is through the
graph constructor.  The constructor calls the to_networkx_graph() function
which attempts to guess the input type and convert it automatically.

Examples
--------
Create a graph with a single edge from a dictionary of dictionaries

>>> d = {0: {1: 1}}  # dict-of-dicts single edge (0,1)
>>> G = nx.Graph(d)

See Also
--------
nx_agraph, nx_pydot
"""

from _typeshed import Incomplete
from collections.abc import Callable, Collection, Iterable

from networkx.classes.graph import Graph, _Data, _EdgeData, _Node, _NodeData
from networkx.utils.backends import _dispatchable

__all__ = [
    "to_networkx_graph",
    "from_dict_of_dicts",
    "to_dict_of_dicts",
    "from_dict_of_lists",
    "to_dict_of_lists",
    "from_edgelist",
    "to_edgelist",
]

def to_networkx_graph(
    data: _Data[_Node],
    create_using: Graph[_Node, _NodeData, _EdgeData] | Callable[[], Graph[_Node, _NodeData, _EdgeData]] | None = None,
    multigraph_input: bool = False,
) -> Graph[_Node, _NodeData, _EdgeData]:
    """
    Make a NetworkX graph from a known data structure.

    The preferred way to call this is automatically
    from the class constructor

    >>> d = {0: {1: {"weight": 1}}}  # dict-of-dicts single edge (0,1)
    >>> G = nx.Graph(d)

    instead of the equivalent

    >>> G = nx.from_dict_of_dicts(d)

    Parameters
    ----------
    data : object to be converted

        Current known types are:
         any NetworkX graph
         dict-of-dicts
         dict-of-lists
         container (e.g. set, list, tuple) of edges
         iterator (e.g. itertools.chain) that produces edges
         generator of edges
         Pandas DataFrame (row per edge)
         2D numpy array
         scipy sparse array
         pygraphviz agraph

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    multigraph_input : bool (default False)
        If True and  data is a dict_of_dicts,
        try to create a multigraph assuming dict_of_dict_of_lists.
        If data and create_using are both multigraphs then create
        a multigraph from a multigraph.
    """
    ...
@_dispatchable
def to_dict_of_lists(G: Graph[_Node], nodelist: Collection[_Node] | None = None) -> dict[_Node, list[_Node]]:
    """
    Returns adjacency representation of graph as a dictionary of lists.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list
       Use only nodes specified in nodelist

    Notes
    -----
    Completely ignores edge data for MultiGraph and MultiDiGraph.
    """
    ...
@_dispatchable
def from_dict_of_lists(
    d: dict[_Node, Iterable[_Node]], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[_Node]: ...
def to_dict_of_dicts(
    G: Graph[_Node], nodelist: Collection[_Node] | None = None, edge_data: float | None = None
) -> dict[Incomplete, Incomplete]: ...
@_dispatchable
def from_dict_of_dicts(
    d: dict[Incomplete, Incomplete],
    create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None,
    multigraph_input: bool = False,
) -> Graph[Incomplete]: ...
@_dispatchable
def to_edgelist(G: Graph[_Node], nodelist: Collection[_Node] | None = None):
    """
    Returns a list of edges in the graph.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list
       Use only nodes specified in nodelist
    """
    ...
@_dispatchable
def from_edgelist(
    edgelist: Iterable[Incomplete], create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None
) -> Graph[Incomplete]: ...
