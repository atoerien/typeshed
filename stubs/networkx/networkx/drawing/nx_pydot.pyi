"""
*****
Pydot
*****

Import and export NetworkX graphs in Graphviz dot format using pydot.

Either this module or nx_agraph can be used to interface with graphviz.

Examples
--------
>>> G = nx.complete_graph(5)
>>> PG = nx.nx_pydot.to_pydot(G)
>>> H = nx.nx_pydot.from_pydot(PG)

See Also
--------
 - pydot:         https://github.com/erocarrera/pydot
 - Graphviz:      https://www.graphviz.org
 - DOT Language:  http://www.graphviz.org/doc/info/lang.html
"""

from _typeshed import SupportsRead, SupportsWrite
from os import PathLike
from typing import Any

from networkx.classes.graph import Graph, _EdgeData, _Node, _NodeData
from networkx.utils.backends import _dispatchable
from pydot import Dot  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]

__all__ = ["write_dot", "read_dot", "graphviz_layout", "pydot_layout", "to_pydot", "from_pydot"]

def write_dot(G: Graph[_Node, _NodeData, _EdgeData], path: str | PathLike[Any] | SupportsWrite[str]) -> None: ...
@_dispatchable
def read_dot(path: str | PathLike[Any] | SupportsRead[str]) -> Graph[str]:
    """
    Returns a NetworkX :class:`MultiGraph` or :class:`MultiDiGraph` from the
    dot file with the passed path.

    If this file contains multiple graphs, only the first such graph is
    returned. All graphs _except_ the first are silently ignored.

    Parameters
    ----------
    path : str or file
        Filename or file handle to read.
        Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    G : MultiGraph or MultiDiGraph
        A :class:`MultiGraph` or :class:`MultiDiGraph`.

    Notes
    -----
    Use `G = nx.Graph(nx.nx_pydot.read_dot(path))` to return a :class:`Graph` instead of a
    :class:`MultiGraph`.
    """
    ...
@_dispatchable
def from_pydot(P: Dot) -> Graph[str]: ...
def to_pydot(N: Graph[_Node, _NodeData, _EdgeData]) -> Dot: ...
def graphviz_layout(
    G: Graph[_Node, _NodeData, _EdgeData], prog: str = "neato", root: _Node | None = None
) -> dict[_Node, tuple[float, float]]: ...
def pydot_layout(
    G: Graph[_Node, _NodeData, _EdgeData], prog: str = "neato", root: _Node | None = None
) -> dict[_Node, tuple[float, float]]: ...
