"""
*************
VF2 Algorithm
*************

An implementation of VF2 algorithm for graph isomorphism testing.

The simplest interface to use this module is to call the
:func:`is_isomorphic <networkx.algorithms.isomorphism.is_isomorphic>`
function.

Introduction
------------

The GraphMatcher and DiGraphMatcher are responsible for matching
graphs or directed graphs in a predetermined manner.  This
usually means a check for an isomorphism, though other checks
are also possible.  For example, a subgraph of one graph
can be checked for isomorphism to a second graph.

Matching is done via syntactic feasibility. It is also possible
to check for semantic feasibility. Feasibility, then, is defined
as the logical AND of the two functions.

To include a semantic check, the (Di)GraphMatcher class should be
subclassed, and the
:meth:`semantic_feasibility <networkx.algorithms.isomorphism.GraphMatcher.semantic_feasibility>`
function should be redefined.  By default, the semantic feasibility function always
returns ``True``.  The effect of this is that semantics are not
considered in the matching of G1 and G2.

Examples
--------

Suppose G1 and G2 are isomorphic graphs. Verification is as follows:

>>> from networkx.algorithms import isomorphism
>>> G1 = nx.path_graph(4)
>>> G2 = nx.path_graph(4)
>>> GM = isomorphism.GraphMatcher(G1, G2)
>>> GM.is_isomorphic()
True

GM.mapping stores the isomorphism mapping from G1 to G2.

>>> GM.mapping
{0: 0, 1: 1, 2: 2, 3: 3}


Suppose G1 and G2 are isomorphic directed graphs.
Verification is as follows:

>>> G1 = nx.path_graph(4, create_using=nx.DiGraph)
>>> G2 = nx.path_graph(4, create_using=nx.DiGraph)
>>> DiGM = isomorphism.DiGraphMatcher(G1, G2)
>>> DiGM.is_isomorphic()
True

DiGM.mapping stores the isomorphism mapping from G1 to G2.

>>> DiGM.mapping
{0: 0, 1: 1, 2: 2, 3: 3}



Subgraph Isomorphism
--------------------
Graph theory literature can be ambiguous about the meaning of the
above statement, and we seek to clarify it now.

In the VF2 literature, a mapping ``M`` is said to be a graph-subgraph
isomorphism iff ``M`` is an isomorphism between ``G2`` and a subgraph of ``G1``.
Thus, to say that ``G1`` and ``G2`` are graph-subgraph isomorphic is to say
that a subgraph of ``G1`` is isomorphic to ``G2``.

Other literature uses the phrase 'subgraph isomorphic' as in '``G1`` does
not have a subgraph isomorphic to ``G2``'.  Another use is as an in adverb
for isomorphic.  Thus, to say that ``G1`` and ``G2`` are subgraph isomorphic
is to say that a subgraph of ``G1`` is isomorphic to ``G2``.

Finally, the term 'subgraph' can have multiple meanings. In this
context, 'subgraph' always means a 'node-induced subgraph'. Edge-induced
subgraph isomorphisms are not directly supported, but one should be
able to perform the check by making use of
:func:`line_graph <networkx.generators.line.line_graph>`. For
subgraphs which are not induced, the term 'monomorphism' is preferred
over 'isomorphism'.

Let ``G = (N, E)`` be a graph with a set of nodes ``N`` and set of edges ``E``.

If ``G' = (N', E')`` is a subgraph, then:
    ``N'`` is a subset of ``N`` and
    ``E'`` is a subset of ``E``.

If ``G' = (N', E')`` is a node-induced subgraph, then:
    ``N'`` is a subset of ``N`` and
    ``E'`` is the subset of edges in ``E`` relating nodes in ``N'``.

If ``G' = (N', E')`` is an edge-induced subgraph, then:
    ``N'`` is the subset of nodes in ``N`` related by edges in ``E'`` and
    ``E'`` is a subset of ``E``.

If ``G' = (N', E')`` is a monomorphism, then:
    ``N'`` is a subset of ``N`` and
    ``E'`` is a subset of the set of edges in ``E`` relating nodes in ``N'``.

Note that if ``G'`` is a node-induced subgraph of ``G``, then it is always a
subgraph monomorphism of ``G``, but the opposite is not always true, as a
monomorphism can have fewer edges.

References
----------
[1]   Luigi P. Cordella, Pasquale Foggia, Carlo Sansone, Mario Vento,
      "A (Sub)Graph Isomorphism Algorithm for Matching Large Graphs",
      IEEE Transactions on Pattern Analysis and Machine Intelligence,
      vol. 26,  no. 10,  pp. 1367-1372,  Oct.,  2004.
      http://ieeexplore.ieee.org/iel5/34/29305/01323804.pdf

[2]   L. P. Cordella, P. Foggia, C. Sansone, M. Vento, "An Improved
      Algorithm for Matching Large Graphs", 3rd IAPR-TC15 Workshop
      on Graph-based Representations in Pattern Recognition, Cuen,
      pp. 149-159, 2001.
      https://www.researchgate.net/publication/200034365_An_Improved_Algorithm_for_Matching_Large_Graphs

See Also
--------
:meth:`semantic_feasibility <networkx.algorithms.isomorphism.GraphMatcher.semantic_feasibility>`
:meth:`syntactic_feasibility <networkx.algorithms.isomorphism.GraphMatcher.syntactic_feasibility>`

Notes
-----

The implementation handles both directed and undirected graphs as well
as multigraphs.

In general, the subgraph isomorphism problem is NP-complete whereas the
graph isomorphism problem is most likely not NP-complete (although no
polynomial-time algorithm is known to exist).
"""

from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ["GraphMatcher", "DiGraphMatcher"]

class GraphMatcher:
    """
    Implementation of VF2 algorithm for matching undirected graphs.

    Suitable for Graph and MultiGraph instances.
    """
    G1: Incomplete
    G2: Incomplete
    G1_nodes: Incomplete
    G2_nodes: Incomplete
    G2_node_order: Incomplete
    old_recursion_limit: Incomplete
    test: str

    def __init__(self, G1, G2) -> None: ...
    def reset_recursion_limit(self) -> None: ...
    def candidate_pairs_iter(self) -> Generator[Incomplete]: ...
    core_1: Incomplete
    core_2: Incomplete
    inout_1: Incomplete
    inout_2: Incomplete
    state: Incomplete
    mapping: Incomplete

    def initialize(self) -> None: ...
    def is_isomorphic(self) -> bool: ...
    def isomorphisms_iter(self) -> Generator[Incomplete, Incomplete]: ...
    def match(self) -> Generator[Incomplete, Incomplete]: ...
    def semantic_feasibility(self, G1_node, G2_node): ...
    def subgraph_is_isomorphic(self): ...
    def subgraph_is_monomorphic(self): ...
    def subgraph_isomorphisms_iter(self) -> Generator[Incomplete, Incomplete]: ...
    def subgraph_monomorphisms_iter(self) -> Generator[Incomplete, Incomplete]: ...
    def syntactic_feasibility(self, G1_node, G2_node): ...

class DiGraphMatcher(GraphMatcher):
    def __init__(self, G1, G2) -> None: ...
    def candidate_pairs_iter(self) -> Generator[Incomplete]: ...
    core_1: Incomplete
    core_2: Incomplete
    in_1: Incomplete
    in_2: Incomplete
    out_1: Incomplete
    out_2: Incomplete
    state: Incomplete
    mapping: Incomplete

    def initialize(self) -> None:
        """
        Reinitializes the state of the algorithm.

        This method should be redefined if using something other than DiGMState.
        If only subclassing GraphMatcher, a redefinition is not necessary.
        """
        ...
    def syntactic_feasibility(self, G1_node, G2_node):
        """
        Returns True if adding (G1_node, G2_node) is syntactically feasible.

        This function returns True if it is adding the candidate pair
        to the current partial isomorphism/monomorphism mapping is allowable.
        The addition is allowable if the inclusion of the candidate pair does
        not make it impossible for an isomorphism/monomorphism to be found.
        """
        ...

class GMState:
    """
    Internal representation of state for the GraphMatcher class.

    This class is used internally by the GraphMatcher class.  It is used
    only to store state specific data. There will be at most G2.order() of
    these objects in memory at a time, due to the depth-first search
    strategy employed by the VF2 algorithm.
    """
    GM: Incomplete
    G1_node: Incomplete
    G2_node: Incomplete
    depth: Incomplete

    def __init__(self, GM, G1_node=None, G2_node=None) -> None:
        """
        Initializes GMState object.

        Pass in the GraphMatcher to which this GMState belongs and the
        new node pair that will be added to the GraphMatcher's current
        isomorphism mapping.
        """
        ...
    def restore(self) -> None:
        """Deletes the GMState object and restores the class variables."""
        ...

class DiGMState:
    """
    Internal representation of state for the DiGraphMatcher class.

    This class is used internally by the DiGraphMatcher class.  It is used
    only to store state specific data. There will be at most G2.order() of
    these objects in memory at a time, due to the depth-first search
    strategy employed by the VF2 algorithm.
    """
    GM: Incomplete
    G1_node: Incomplete
    G2_node: Incomplete
    depth: Incomplete

    def __init__(self, GM, G1_node=None, G2_node=None) -> None:
        """
        Initializes DiGMState object.

        Pass in the DiGraphMatcher to which this DiGMState belongs and the
        new node pair that will be added to the GraphMatcher's current
        isomorphism mapping.
        """
        ...
    def restore(self) -> None:
        """Deletes the DiGMState object and restores the class variables."""
        ...
