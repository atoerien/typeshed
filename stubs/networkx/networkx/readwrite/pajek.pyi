"""
*****
Pajek
*****
Read graphs in Pajek format.

This implementation handles directed and undirected graphs including
those with self loops and parallel edges.

Format
------
See http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm
for format information.
"""

from _typeshed import Incomplete
from collections.abc import Generator

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["read_pajek", "parse_pajek", "generate_pajek", "write_pajek"]

def generate_pajek(G: Graph[_Node]) -> Generator[Incomplete]: ...
def write_pajek(G: Graph[_Node], path, encoding: str = "UTF-8") -> None: ...
@_dispatchable
def read_pajek(path, encoding: str = "UTF-8"):
    """
    Read graph in Pajek format from path.

    Parameters
    ----------
    path : file or string
       Filename or file handle to read.
       Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    G : NetworkX MultiGraph or MultiDiGraph.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.write_pajek(G, "test.net")
    >>> G = nx.read_pajek("test.net")

    To create a Graph instead of a MultiGraph use

    >>> G1 = nx.Graph(G)

    References
    ----------
    See http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm
    for format information.
    """
    ...
@_dispatchable
def parse_pajek(lines):
    """
    Parse Pajek format graph from string or iterable.

    Parameters
    ----------
    lines : string or iterable
       Data in Pajek format.

    Returns
    -------
    G : NetworkX graph

    See Also
    --------
    read_pajek
    """
    ...
def make_qstr(t):
    """
    Returns the string representation of t.
    Add outer double-quotes if the string has a space.
    """
    ...
