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
) -> Graph[str]: ...
def to_agraph(N: Graph[_Node, _NodeData, _EdgeData]) -> AGraph: ...
def write_dot(
    G: Graph[_Node, _NodeData, _EdgeData],
    path: str | IO[str] | IO[bytes] | _SupportsOpen[OpenTextModeWriting, IO[str] | IO[bytes]],
) -> None: ...
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
) -> dict[_Node, tuple[float, float]]: ...
def pygraphviz_layout(
    G: Graph[_Node, _NodeData, _EdgeData], prog: str = "neato", root: str | None = None, args: str = ""
) -> dict[_Node, tuple[float, float]]: ...
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
