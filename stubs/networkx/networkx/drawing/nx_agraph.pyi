"""
***************
Graphviz AGraph
***************

Interface to pygraphviz AGraph class.

Examples
--------
>>> G = nx.complete_graph(5)
>>> A = nx.nx_agraph.to_agraph(G)
>>> H = nx.nx_agraph.from_agraph(A)

See Also
--------
 - Pygraphviz: http://pygraphviz.github.io/
 - Graphviz:      https://www.graphviz.org
 - DOT Language:  http://www.graphviz.org/doc/info/lang.html
"""

from _typeshed import OpenBinaryModeUpdating, OpenTextModeReading, OpenTextModeWriting, SupportsWrite
from collections.abc import Callable
from typing import IO, Any, Protocol, TypeVar, type_check_only

from networkx.classes.graph import Graph, _EdgeData, _Node, _NodeData
from networkx.utils.backends import _dispatchable
from pygraphviz.agraph import AGraph  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]

__all__ = ["from_agraph", "to_agraph", "write_dot", "read_dot", "graphviz_layout", "pygraphviz_layout", "view_pygraphviz"]

_ModeT_contra = TypeVar("_ModeT_contra", bound=str, contravariant=True)
_FileT_co = TypeVar("_FileT_co", covariant=True)

@type_check_only
class _SupportsOpen(Protocol[_ModeT_contra, _FileT_co]):
    def open(self, *, mode: _ModeT_contra) -> _FileT_co: ...

@_dispatchable
def from_agraph(
    A: AGraph, create_using: Graph[str] | type[Graph[str]] | None = None  # TODO: add overloads on `create_using`
) -> Graph[str]:
    """
    Returns a NetworkX Graph or DiGraph from a PyGraphviz graph.

    Parameters
    ----------
    A : PyGraphviz AGraph
      A graph created with PyGraphviz

    create_using : NetworkX graph constructor, optional (default=None)
       Graph type to create. If graph instance, then cleared before populated.
       If `None`, then the appropriate Graph type is inferred from `A`.

    Examples
    --------
    >>> K5 = nx.complete_graph(5)
    >>> A = nx.nx_agraph.to_agraph(K5)
    >>> G = nx.nx_agraph.from_agraph(A)

    Notes
    -----
    The Graph G will have a dictionary G.graph_attr containing
    the default graphviz attributes for graphs, nodes and edges.

    Default node attributes will be in the dictionary G.node_attr
    which is keyed by node.

    Edge attributes will be returned as edge data in G.  With
    edge_attr=False the edge data will be the Graphviz edge weight
    attribute or the value 1 if no edge weight attribute is found.
    """
    ...
def to_agraph(N: Graph[_Node, _NodeData, _EdgeData]) -> AGraph:
    """
    Returns a pygraphviz graph from a NetworkX graph N.

    Parameters
    ----------
    N : NetworkX graph
      A graph created with NetworkX

    Examples
    --------
    >>> K5 = nx.complete_graph(5)
    >>> A = nx.nx_agraph.to_agraph(K5)

    Notes
    -----
    If N has an dict N.graph_attr an attempt will be made first
    to copy properties attached to the graph (see from_agraph)
    and then updated with the calling arguments if any.
    """
    ...
def write_dot(
    G: Graph[_Node, _NodeData, _EdgeData],
    path: str | IO[str] | IO[bytes] | _SupportsOpen[OpenTextModeWriting, IO[str] | IO[bytes]],
) -> None:
    """
    Write NetworkX graph G to Graphviz dot format on path.

    Parameters
    ----------
    G : graph
       A networkx graph
    path : filename
       Filename or file handle to write

    Notes
    -----
    To use a specific graph layout, call ``A.layout`` prior to `write_dot`.
    Note that some graphviz layouts are not guaranteed to be deterministic,
    see https://gitlab.com/graphviz/graphviz/-/issues/1767 for more info.
    """
    ...
@_dispatchable
def read_dot(path: str | IO[str] | IO[bytes] | _SupportsOpen[OpenTextModeReading, IO[str] | IO[bytes]]) -> Graph[str]:
    """
    Returns a NetworkX graph from a dot file on path.

    Parameters
    ----------
    path : file or string
       File name or file handle to read.
    """
    ...
def graphviz_layout(
    G: Graph[_Node, _NodeData, _EdgeData], prog: str = "neato", root: str | None = None, args: str = ""
) -> dict[_Node, tuple[float, float]]:
    """
    Create node positions for G using Graphviz.

    Parameters
    ----------
    G : NetworkX graph
      A graph created with NetworkX
    prog : string
      Name of Graphviz layout program
    root : string, optional
      Root node for twopi layout
    args : string, optional
      Extra arguments to Graphviz layout program

    Returns
    -------
    Dictionary of x, y, positions keyed by node.

    Examples
    --------
    >>> G = nx.petersen_graph()
    >>> pos = nx.nx_agraph.graphviz_layout(G)
    >>> pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    Notes
    -----
    This is a wrapper for pygraphviz_layout.

    Note that some graphviz layouts are not guaranteed to be deterministic,
    see https://gitlab.com/graphviz/graphviz/-/issues/1767 for more info.
    """
    ...
def pygraphviz_layout(
    G: Graph[_Node, _NodeData, _EdgeData], prog: str = "neato", root: str | None = None, args: str = ""
) -> dict[_Node, tuple[float, float]]:
    """
    Create node positions for G using Graphviz.

    Parameters
    ----------
    G : NetworkX graph
      A graph created with NetworkX
    prog : string
      Name of Graphviz layout program
    root : string, optional
      Root node for twopi layout
    args : string, optional
      Extra arguments to Graphviz layout program

    Returns
    -------
    node_pos : dict
      Dictionary of x, y, positions keyed by node.

    Examples
    --------
    >>> G = nx.petersen_graph()
    >>> pos = nx.nx_agraph.graphviz_layout(G)
    >>> pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    Notes
    -----
    If you use complex node objects, they may have the same string
    representation and GraphViz could treat them as the same node.
    The layout may assign both nodes a single location. See Issue #1568
    If this occurs in your case, consider relabeling the nodes just
    for the layout computation using something similar to::

        >>> H = nx.convert_node_labels_to_integers(G, label_attribute="node_label")
        >>> H_layout = nx.nx_agraph.pygraphviz_layout(H, prog="dot")
        >>> G_layout = {H.nodes[n]["node_label"]: p for n, p in H_layout.items()}

    Note that some graphviz layouts are not guaranteed to be deterministic,
    see https://gitlab.com/graphviz/graphviz/-/issues/1767 for more info.
    """
    ...
def view_pygraphviz(
    G: Graph[_Node, _NodeData, _EdgeData],
    # From implementation looks like Callable could return object since it's always immediately stringified
    # But judging by documentation this seems like an extra runtime safety thing and not intended
    # Leaving as str unless anyone reports a valid use-case
    edgelabel: str | Callable[[dict[str, Any]], str] | None = None,
    prog: str = "dot",
    args: str = "",
    suffix: str = "",
    path: str | SupportsWrite[bytes] | _SupportsOpen[OpenBinaryModeUpdating, SupportsWrite[bytes]] | None = None,
    show: bool = True,
) -> tuple[str, AGraph]:
    """
    Views the graph G using the specified layout algorithm.

    Parameters
    ----------
    G : NetworkX graph
        The machine to draw.
    edgelabel : str, callable, None
        If a string, then it specifies the edge attribute to be displayed
        on the edge labels. If a callable, then it is called for each
        edge and it should return the string to be displayed on the edges.
        The function signature of `edgelabel` should be edgelabel(data),
        where `data` is the edge attribute dictionary.
    prog : string
        Name of Graphviz layout program.
    args : str
        Additional arguments to pass to the Graphviz layout program.
    suffix : str
        If `filename` is None, we save to a temporary file.  The value of
        `suffix` will appear at the tail end of the temporary filename.
    path : str, None
        The filename used to save the image.  If None, save to a temporary
        file.  File formats are the same as those from pygraphviz.agraph.draw.
        Filenames ending in .gz or .bz2 will be compressed.
    show : bool, default = True
        Whether to display the graph with :mod:`PIL.Image.show`,
        default is `True`. If `False`, the rendered graph is still available
        at `path`.

    Returns
    -------
    path : str
        The filename of the generated image.
    A : PyGraphviz graph
        The PyGraphviz graph instance used to generate the image.

    Notes
    -----
    If this function is called in succession too quickly, sometimes the
    image is not displayed. So you might consider time.sleep(.5) between
    calls if you experience problems.

    Note that some graphviz layouts are not guaranteed to be deterministic,
    see https://gitlab.com/graphviz/graphviz/-/issues/1767 for more info.
    """
    ...
