"""
Provides a function for computing the extendability of a graph which is
undirected, simple, connected and bipartite and contains at least one perfect matching.
"""

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["maximal_extendability"]

@_dispatchable
def maximal_extendability(G: Graph[_Node]) -> int: ...
