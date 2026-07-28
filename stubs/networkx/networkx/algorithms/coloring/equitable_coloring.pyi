"""Equitable coloring of graphs with bounded degree."""

from _typeshed import Incomplete, SupportsGetItem
from collections.abc import Mapping
from typing import SupportsIndex

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["equitable_color"]

@_dispatchable
def is_coloring(G: Graph[_Node], coloring: SupportsGetItem[Incomplete, Incomplete]) -> bool:
    """Determine if the coloring is a valid coloring for the graph G."""
    ...
@_dispatchable
def is_equitable(G: Graph[_Node], coloring: Mapping[Incomplete, Incomplete], num_colors: SupportsIndex | None = None) -> bool:
    """Determines if the coloring is valid and equitable for the graph G."""
    ...
def make_C_from_F(F): ...
def make_N_from_L_C(L, C): ...
def make_H_from_C_N(C, N): ...
def change_color(u, X, Y, N, H, F, C, L):
    """Change the color of 'u' from X to Y and update N, H, F, C."""
    ...
def move_witnesses(src_color, dst_color, N, H, F, C, T_cal, L):
    """Move witness along a path from src_color to dst_color."""
    ...
@_dispatchable
def pad_graph(G: Graph[_Node], num_colors):
    """
    Add a disconnected complete clique K_p such that the number of nodes in
    the graph becomes a multiple of `num_colors`.

    Assumes that the graph's nodes are labelled using integers.

    Returns the number of nodes with each color.
    """
    ...
def procedure_P(V_minus, V_plus, N, H, F, C, L, excluded_colors=None):
    """Procedure P as described in the paper."""
    ...
@_dispatchable
def equitable_color(G: Graph[_Node], num_colors: int) -> dict[Incomplete, Incomplete]: ...
