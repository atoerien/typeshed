from _typeshed import Incomplete, StrPath, SupportsRead

from networkx.classes.graph import Graph, _Node
from networkx.classes.multidigraph import MultiDiGraph
from networkx.utils.backends import _dispatchable

def write_p2g(G: Graph[_Node], path, encoding: str = "utf-8") -> None:
    """
    Write NetworkX graph in p2g format.

    Notes
    -----
    This format is meant to be used with directed graphs with
    possible self loops.
    """
    ...
@_dispatchable
def read_p2g(path: StrPath | SupportsRead[str], encoding: str = "utf-8") -> MultiDiGraph[Incomplete]: ...
@_dispatchable
def parse_p2g(lines) -> MultiDiGraph[Incomplete]:
    """
    Parse p2g format graph from string or iterable.

    Returns
    -------
    MultiDiGraph
    """
    ...
