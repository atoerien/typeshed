"""Mixing matrices for node attributes and degree."""

from _typeshed import Incomplete
from collections.abc import Iterable, Mapping

import numpy as np
from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["attribute_mixing_matrix", "attribute_mixing_dict", "degree_mixing_matrix", "degree_mixing_dict", "mixing_dict"]

@_dispatchable
def attribute_mixing_dict(
    G: Graph[_Node], attribute: str, nodes: Iterable[Incomplete] | None = None, normalized: bool = False
) -> dict[Incomplete, Incomplete]:
    """
    Returns dictionary representation of mixing matrix for attribute.

    Parameters
    ----------
    G : graph
       NetworkX graph object.

    attribute : string
       Node attribute key.

    nodes: list or iterable (optional)
        Unse nodes in container to build the dict. The default is all nodes.

    normalized : bool (default=False)
       Return counts if False or probabilities if True.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_nodes_from([0, 1], color="red")
    >>> G.add_nodes_from([2, 3], color="blue")
    >>> G.add_edge(1, 3)
    >>> d = nx.attribute_mixing_dict(G, "color")
    >>> print(d["red"]["blue"])
    1
    >>> print(d["blue"]["red"])  # d symmetric for undirected graphs
    1

    Returns
    -------
    d : dictionary
       Counts or joint probability of occurrence of attribute pairs.
    """
    ...
@_dispatchable
def attribute_mixing_matrix(
    G: Graph[_Node],
    attribute: str,
    nodes: Iterable[Incomplete] | None = None,
    mapping: Mapping[Incomplete, Incomplete] | None = None,
    normalized: bool = True,
) -> np.ndarray[Incomplete, Incomplete]: ...
@_dispatchable
def degree_mixing_dict(
    G: Graph[_Node], x: str = "out", y: str = "in", weight: str | None = None, nodes=None, normalized: bool = False
) -> dict[Incomplete, Incomplete]:
    """
    Returns dictionary representation of mixing matrix for degree.

    Parameters
    ----------
    G : graph
        NetworkX graph object.

    x: string ('in','out')
       The degree type for source node (directed graphs only).

    y: string ('in','out')
       The degree type for target node (directed graphs only).

    weight: string or None, optional (default=None)
       The edge attribute that holds the numerical value used
       as a weight.  If None, then each edge has weight 1.
       The degree is the sum of the edge weights adjacent to the node.

    normalized : bool (default=False)
        Return counts if False or probabilities if True.

    Returns
    -------
    d: dictionary
       Counts or joint probability of occurrence of degree pairs.
    """
    ...
@_dispatchable
def degree_mixing_matrix(
    G: Graph[_Node],
    x: str = "out",
    y: str = "in",
    weight: str | None = None,
    nodes: Iterable[Incomplete] | None = None,
    normalized: bool = True,
    mapping: Mapping[Incomplete, Incomplete] | None = None,
) -> np.ndarray[Incomplete, Incomplete]: ...
@_dispatchable
def mixing_dict(xy: Iterable[tuple[Incomplete, Incomplete]], normalized: bool = False) -> dict[Incomplete, Incomplete]: ...
