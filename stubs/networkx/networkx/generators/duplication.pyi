"""
Functions for generating graphs based on the "duplication" method.

These graph generators start with a small initial graph then duplicate
nodes and (partially) duplicate their edges. These functions are
generally inspired by biological networks.
"""

from _typeshed import Incomplete

from networkx.utils.backends import _dispatchable

from ..classes.graph import Graph

__all__ = ["partial_duplication_graph", "duplication_divergence_graph"]

@_dispatchable
def partial_duplication_graph(N: int, n: int, p: float, q: float, seed=None): ...
@_dispatchable
def duplication_divergence_graph(n: int, p: float, seed=None) -> Graph[Incomplete]: ...
