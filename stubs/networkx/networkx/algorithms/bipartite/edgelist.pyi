from _typeshed import Incomplete, StrPath, SupportsRead, SupportsWrite
from collections.abc import Collection, Generator, Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["generate_edgelist", "write_edgelist", "parse_edgelist", "read_edgelist"]

@_dispatchable
def write_edgelist(
    G: Graph[_Node],
    path: StrPath | SupportsWrite[bytes],
    comments: str = "#",
    delimiter: str = " ",
    data: bool = True,
    encoding: str = "utf-8",
) -> None: ...
@_dispatchable
def generate_edgelist(G: Graph[_Node], delimiter: str = " ", data: bool = True) -> Generator[str]:
    """
    Generate a single line of the bipartite graph G in edge list format.

    Parameters
    ----------
    G : NetworkX graph
       The graph is assumed to have node attribute `part` set to 0,1 representing
       the two graph parts

    delimiter : string, optional
       Separator for node labels

    data : bool or list of keys
       If False generate no edge data.  If True use a dictionary
       representation of edge data.  If a list of keys use a list of data
       values corresponding to the keys.

    Returns
    -------
    lines : string
        Lines of data in adjlist format.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.path_graph(4)
    >>> G.add_nodes_from([0, 2], bipartite=0)
    >>> G.add_nodes_from([1, 3], bipartite=1)
    >>> G[1][2]["weight"] = 3
    >>> G[2][3]["capacity"] = 12
    >>> for line in bipartite.generate_edgelist(G, data=False):
    ...     print(line)
    0 1
    2 1
    2 3

    >>> for line in bipartite.generate_edgelist(G):
    ...     print(line)
    0 1 {}
    2 1 {'weight': 3}
    2 3 {'capacity': 12}

    >>> for line in bipartite.generate_edgelist(G, data=["weight"]):
    ...     print(line)
    0 1
    2 1 3
    2 3
    """
    ...
@_dispatchable
def parse_edgelist(
    lines: Iterable[str],
    comments: str | None = "#",
    delimiter: str | None = None,
    create_using: Graph[_Node] | type[Graph[_Node]] | None = None,
    nodetype: type[Incomplete] | None = None,
    data: bool | Collection[tuple[str, type[Incomplete]]] = True,
) -> Graph[Incomplete]: ...
@_dispatchable
def read_edgelist(
    path: StrPath | SupportsRead[bytes],
    comments: str | None = "#",
    delimiter: str | None = None,
    create_using: Graph[Incomplete] | type[Graph[Incomplete]] | None = None,
    nodetype=None,
    data: bool | Collection[tuple[str, type[Incomplete]]] = True,
    edgetype=None,
    encoding: str | None = "utf-8",
) -> Graph[Incomplete]: ...
