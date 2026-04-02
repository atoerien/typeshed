"""
ISMAGS Algorithm
================

Provides a Python implementation of the ISMAGS algorithm. [1]_

ISMAGS does a symmetry analysis to find the constraints on isomorphisms if
we preclude yielding isomorphisms that differ by a symmetry of the subgraph.
For example, if the subgraph contains a 4-cycle, every isomorphism would have a
symmetric version with the nodes rotated relative to the original isomorphism.
By encoding these symmetries as constraints we reduce the search space for
isomorphisms and we also simplify processing the resulting isomorphisms.

ISMAGS finds (subgraph) isomorphisms between two graphs, taking the
symmetry of the subgraph into account. In most cases the VF2 algorithm is
faster (at least on small graphs) than this implementation, but in some cases
there are an exponential number of isomorphisms that are symmetrically
equivalent. In that case, the ISMAGS algorithm will provide only one isomorphism
per symmetry group, speeding up finding isomorphisms and avoiding the task of
post-processing many effectively identical isomorphisms.

>>> petersen = nx.petersen_graph()
>>> ismags = nx.isomorphism.ISMAGS(petersen, petersen)
>>> isomorphisms = list(ismags.isomorphisms_iter(symmetry=False))
>>> len(isomorphisms)
120
>>> isomorphisms = list(ismags.isomorphisms_iter(symmetry=True))
>>> answer = [{0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}]
>>> answer == isomorphisms
True

In addition, this implementation also provides an interface to find the
largest common induced subgraph [2]_ between any two graphs, again taking
symmetry into account. Given ``graph`` and ``subgraph`` the algorithm will remove
nodes from the ``subgraph`` until ``subgraph`` is isomorphic to a subgraph of
``graph``. Since only the symmetry of ``subgraph`` is taken into account it is
worth thinking about how you provide your graphs:

>>> graph1 = nx.path_graph(4)
>>> graph2 = nx.star_graph(3)
>>> ismags = nx.isomorphism.ISMAGS(graph1, graph2)
>>> ismags.is_isomorphic()
False
>>> largest_common_subgraph = list(ismags.largest_common_subgraph())
>>> answer = [{1: 0, 0: 1, 2: 2}, {2: 0, 1: 1, 3: 2}]
>>> answer == largest_common_subgraph
True
>>> ismags2 = nx.isomorphism.ISMAGS(graph2, graph1)
>>> largest_common_subgraph = list(ismags2.largest_common_subgraph())
>>> answer = [
...     {1: 0, 0: 1, 2: 2},
...     {1: 0, 0: 1, 3: 2},
...     {2: 0, 0: 1, 1: 2},
...     {2: 0, 0: 1, 3: 2},
...     {3: 0, 0: 1, 1: 2},
...     {3: 0, 0: 1, 2: 2},
... ]
>>> answer == largest_common_subgraph
True

However, when not taking symmetry into account, it doesn't matter:

>>> largest_common_subgraph = list(ismags.largest_common_subgraph(symmetry=False))
>>> answer = [
...     {1: 0, 0: 1, 2: 2},
...     {1: 0, 2: 1, 0: 2},
...     {2: 0, 1: 1, 3: 2},
...     {2: 0, 3: 1, 1: 2},
...     {1: 0, 0: 1, 2: 3},
...     {1: 0, 2: 1, 0: 3},
...     {2: 0, 1: 1, 3: 3},
...     {2: 0, 3: 1, 1: 3},
...     {1: 0, 0: 2, 2: 3},
...     {1: 0, 2: 2, 0: 3},
...     {2: 0, 1: 2, 3: 3},
...     {2: 0, 3: 2, 1: 3},
... ]
>>> answer == largest_common_subgraph
True
>>> largest_common_subgraph = list(ismags2.largest_common_subgraph(symmetry=False))
>>> answer = [
...     {1: 0, 0: 1, 2: 2},
...     {1: 0, 0: 1, 3: 2},
...     {2: 0, 0: 1, 1: 2},
...     {2: 0, 0: 1, 3: 2},
...     {3: 0, 0: 1, 1: 2},
...     {3: 0, 0: 1, 2: 2},
...     {1: 1, 0: 2, 2: 3},
...     {1: 1, 0: 2, 3: 3},
...     {2: 1, 0: 2, 1: 3},
...     {2: 1, 0: 2, 3: 3},
...     {3: 1, 0: 2, 1: 3},
...     {3: 1, 0: 2, 2: 3},
... ]
>>> answer == largest_common_subgraph
True

Notes
-----
- Node and edge equality is assumed to be transitive: if A is equal to B, and
  B is equal to C, then A is equal to C.

- With a method that yields subgraph isomorphisms, we can construct functions like
  ``is_subgraph_isomorphic`` by checking for any yielded mapping. And functions like
  ``is_isomorphic`` by checking whether the subgraph has the same number of nodes as
  the graph and is also subgraph isomorphic. This subpackage also allows a
  ``symmetry`` bool keyword argument so you can find isomorphisms with or
  without the symmetry constraints.

- For more information, see [2]_ and the documentation for :class:`ISMAGS`
  which includes a description of the algorithm.

References
----------
.. [1] M. Houbraken, S. Demeyer, T. Michoel, P. Audenaert, D. Colle,
   M. Pickavet, "The Index-Based Subgraph Matching Algorithm with General
   Symmetries (ISMAGS): Exploiting Symmetry for Faster Subgraph
   Enumeration", PLoS One 9(5): e97896, 2014.
   https://doi.org/10.1371/journal.pone.0097896
.. [2] https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph
"""

from _typeshed import Incomplete
from collections.abc import Callable, Generator, Hashable, Iterable
from typing import Any

__all__ = ["ISMAGS"]

def are_all_equal(iterable: Iterable[Any]) -> bool:
    """
    Returns ``True`` if and only if all elements in `iterable` are equal; and
    ``False`` otherwise.

    Parameters
    ----------
    iterable: collections.abc.Iterable
        The container whose elements will be checked.

    Returns
    -------
    bool
        ``True`` iff all elements in `iterable` compare equal, ``False``
        otherwise.
    """
    ...
def make_partition(
    items: Iterable[Hashable], test: Callable[[Hashable, Hashable], bool], check: bool = True
) -> list[set[Incomplete]]:
    """
    Partitions items into sets based on the outcome of ``test(item1, item2)``.
    Pairs of items for which `test` returns `True` end up in the same set.

    Parameters
    ----------
    items : collections.abc.Iterable[collections.abc.Hashable]
        Items to partition
    test : collections.abc.Callable[collections.abc.Hashable, collections.abc.Hashable]
        A function that will be called with 2 arguments, taken from items.
        Should return `True` if those 2 items match/tests so need to end up in the same
        part of the partition, and `False` otherwise.
    check : bool optional (default: True)
        If ``True``, check that the resulting partition satisfies the match criteria.
        Every item should match every item in its part and none outside the part.

    Returns
    -------
    list[set]
        A partition as a list of sets (the parts). Each set contains some of
        the items in `items`, such that all items are in exactly one part and every
        pair of items in each part matches. The following will be true:
        ``all(thing_matcher(*pair) for pair in itertools.combinations(items, 2))``

    Notes
    -----
    The function `test` is assumed to be transitive: if ``test(a, b)`` and
    ``test(b, c)`` return ``True``, then ``test(a, c)`` must also be ``True``.
    The function `test` is assumed to be commutative: if ``test(a, b)``
    returns ``True`` then ``test(b, a)`` returns ``True``.
    """
    ...
def node_to_part_ID_dict(partition: Iterable[Iterable[Incomplete]]) -> dict[Incomplete, int]:
    """
    Creates a dictionary that maps each item in each part to the index of
    the part to which it belongs.

    Parameters
    ----------
    partition: collections.abc.Sequence[collections.abc.Iterable]
        As returned by :func:`make_partition`.

    Returns
    -------
    dict
    """
    ...
def color_degree_by_node(G, n_colors, e_colors):
    """
    Returns a dict by node to counts of edge and node color for that node.

    This returns a dict by node to a 2-tuple of node color and degree by
    (edge color and nbr color). E.g. ``{0: (1, {(0, 2): 5})}`` means that
    node ``0`` has node type 1 and has 5 edges of type 0 that go to nodes of type 2.
    Thus, this is a measure of degree (edge count) by color of edge and color
    of the node on the other side of that edge.

    For directed graphs the degree counts is a 2-tuple of (in, out) degree counts.

    Ideally, if edge_match is None, this could get simplified to just the node
    color on the other end of the edge. Similarly if node_match is None then only
    edge color is tracked. And if both are None, we simply count the number of edges.
    """
    ...

class EdgeLookup:
    """
    Class to handle getitem for undirected edges.

    Note that ``items()`` iterates over one of the two representations of the edge
    (u, v) and (v, u). So this technically doesn't violate the Mapping
    invariant that (k,v) pairs reported by ``items()`` satisfy ``.__getitem__(k) == v``.
    But we are violating the spirit of the protocol by having keys available
    for lookup by ``__getitem__`` that are not reported by ``items()``.

    Note that if we used frozensets for undirected edges we would have the same
    behavior we see here. You could ``__getitem__`` either ``{u, v}`` or ``{v, u}``
    and get the same value -- yet ``items()`` would only report one of the two.
    So from that perspective we *are* following the Mapping protocol. Our keys
    are undirected edges. We are using 2-tuples as an imperfect representation
    of these edges. We are not using 2-tuples as keys. Only as imperfect edges
    and we use the edges as keys.
    """
    edge_dict: Incomplete
    def __init__(self, edge_dict) -> None: ...
    def __getitem__(self, edge): ...
    def items(self): ...

class ISMAGS:
    """
    Implements the ISMAGS subgraph matching algorithm. [1]_ ISMAGS stands for
    "Index-based Subgraph Matching Algorithm with General Symmetries". As the
    name implies, it is symmetry aware and will only generate non-symmetric
    isomorphisms.

    Attributes
    ----------
    graph: networkx.Graph
    subgraph: networkx.Graph

    Notes
    -----
    ISMAGS does a symmetry analysis to find the constraints on isomorphisms if
    we preclude yielding isomorphisms that differ by a symmetry of the subgraph.
    For example, if the subgraph is a 4-cycle, every isomorphism would have a
    symmetric version with the nodes rotated relative to the original isomorphism.
    By encoding these symmetries as constraints we reduce the search space for
    isomorphisms and we also simplify processing the resulting isomorphisms.

    **Symmetry Analysis**

    The constraints in ISMAGS are based off the handling in ``nauty`` and its many
    variants, in particular ``saucy``, as discussed in the ISMAGS paper [1]_.
    That paper cites [3]_ for details on symmetry handling. Figure 2 of [3]_
    describes the DFS approach to symmetries used here and relying on a data structure
    called an Ordered Pair Partitions(OPP). This consists of a pair of partitions
    where each part represents nodes with the same degree-by-color over all colors.
    We refine these partitions simultaneously in a way to result in permutations
    of the nodes that preserve the graph structure. We thus find automorphisms
    for the subgraph of interest. From those we identify pairs of nodes which
    are structurally equivalent. We then constrain our problem by requiring the
    first of the pair to always be assigned first in the isomorphism -- thus
    constraining the isomorphisms reported to only one example from the set of all
    symmetrically equivalent isomorphisms. These constraints are computed once
    based on the subgraph symmetries and then used throughout the DFS search for
    isomorphisms.

    Finding the symmetries involves a DFS of the OPP wherein we "couple" a node
    to a node in its degree-by-color part of the partition. This "coupling" is done
    via assigning a new color in the top partition to the node being coupled,
    and the same new color in the bottom partition to the node being coupled to.
    This new color has only one node in each partition. The new color also requires
    that we "refine" both top and bottom partitions by splitting parts until each
    part represents a common degree-by-color value. Those refinements introduce
    new colors as the parts are split during refinement. Parts do not get combined
    during refinement. So the coupling/refining process always results in at least
    one new part with only one node in both the top and bottom partition. In practice
    we usually refine into many new one-node parts in both partitions.
    We continue in this way until each node has its own part/color in the top partition
    -- and the node in the bottom partition with that color is the symmetric node.
    That is, an OPP represents an automorphism, and thus a symmetry
    of the subgraph when each color has a single node in the top partition and a single
    node in the bottom partition. From those automorphisms we build up a set of nodes
    that can be obtained from each other by symmetry (they are mutually symmetric).
    That set of nodes is called an "orbit" of the subgraph under symmetry.

    After finding the orbits for one symmetry, we backtrack in the DFS by removing the
    latest coupling and replacing it with a coupling from the same top node to a new
    bottom node in its degree-by-color grouping. When all possible couplings for that
    node are considered we backtrack to the previously coupled node and recouple in
    a DFS manner.

    We can prune the DFS search tree in helpful ways. The paper [2]_ demonstrates 6
    situations of interest in the DFS where pruning is possible:

    - An **Automorphism OPP** is an OPP where every part in both partitions
      contains a single node. The mapping/automorphism is found by mapping
      each top node to the bottom node in the same color part. For example,
      ``[({1}, {2}, {3}); ({2}, {3}, {1})]`` represents the mapping of each
      node to the next in a triangle. It rotates the nodes around the triangle.
    - The **Identity OPP** is the first automorphism found during the DFS. It
      appears on the left side of the DFS tree and is first due to our ordering of
      coupling nodes to be in an arbitrary but fixed ordering of the nodes. This
      automorphism does not show any symmetries, but it ensures the orbit for each
      node includes itself and it sets us up for handling the symmetries. Note that
      a subgraph with no symmetries will only have the identity automorphism.
    - A **Non-isomorphic OPP** occurs when refinement creates a different number of
      parts in the top partition than in the bottom partition. This means no symmetries
      will be found during further processing of that subtree of the DFS. We prune
      the subtree and continue.
    - A **Matching OPP** is such that each top part that has more than one node is
      in fact equal to the bottom part with the same color. The many-node-parts match
      exactly. The single-node parts then represent symmetries that do not permute
      any matching nodes. Matching OPPs arise while finding the Identity Mapping. But
      the single-node parts are identical in the two partitions, so no useful symmetries
      are found. But after the Identity Mapping is found, every Matching OPP encountered
      will have different nodes in at least two single-node parts of the same color.
      So these positions in the DFS provide us with symmetries without any
      need to find the whole automorphism. We can prune the subtree, update the orbits
      and backtrack. Any larger symmetries that combine these symmetries with symmetries
      of the many-node-parts do not need to be explored because the symmetry "generators"
      found in this way provide a basis for all symmetries. We will find the symmetry
      generators of the many-node-parts at another subtree of the DFS.
    - An **Orbit Pruning OPP** is an OPP where the node coupling to be considered next
      has both nodes already known to be in the same orbit. We have already identified
      those permutations when we discovered the orbit. So we can prune the resulting
      subtree. This is the primary pruning discussed in [1]_.
    - A **Coset Point** in the DFS is a point of the tree when a node is first
      back-tracked. That is, its couplings have all been analyzed once and we backtrack
      to its parent. So, said another way, when a node is backtracked to and is about to
      be mapped to a different node for the first time, its child in the DFS has been
      completely analysed. Thus the orbit for that child at this point in the DFS is
      the full orbit for symmetries involving only that child or larger nodes in the
      node order. All smaller nodes are mapped to themselves.
      This orbit is due to symmetries not involving smaller nodes. Such an orbit is
      called the "coset" of that node. The Coset Point does not lead to pruning or to
      more symmetries. It is the point in the process where we store the **coset** of
      the node being backtracked. We use the cosets to construct the symmetry
      constraints.

    Once the pruned DFS tree has been traversed, we have collected the cosets of some
    special nodes. Often most nodes are not coupled during the progression down the left
    side of the DFS. They are separated from other nodes during the partition refinement
    process after coupling. So they never get coupled directly. Thus the number of cosets
    we find is typically many fewer than the number of nodes.

    We turn those cosets into constraints on the nodes when building non-symmetric
    isomorphisms. The node whose coset is used is paired with each other node in the
    coset. These node-pairs form the constraints. During isomorphism construction we
    always select the first of the constraint before the other. This removes subtrees
    from the DFS traversal space used to build isomorphisms.

    The constraints we obtain via symmetry analysis of the subgraph are used for
    finding non-symmetric isomorphisms. We prune the isomorphism tree based on
    the constraints we obtain from the symmetry analysis.

    **Isomorphism Construction**

    Once we have symmetry constraints on the isomorphisms, ISMAGS constructs the allowed
    isomorphisms by mapping each node of the subgraph to all possible nodes (with the
    same degree-by-color) from the graph. We partition all nodes into degree-by-color
    parts and order the subgraph nodes we consider using smallest part size first.
    The idea is to try to map the most difficult subgraph nodes first (most difficult
    here means least number of graph candidates).

    By considering each potential subgraph node to graph candidate mapping image in turn,
    we perform a DFS traversal of partial mappings. If the mapping is rejected due to
    the graph neighbors not matching the degree-by-color of the subgraph neighbors, or
    rejected due to the constraints imposed from symmetry, we prune that subtree and
    consider a new graph candidate node for that subgraph node. When no more graph
    candidates remain we backtrack to the previous node in the mapping and consider a
    new graph candidate for that node. If we ever get to a depth where all subgraph nodes
    are mapped and no structural requirements or symmetry constraints are violated,
    we have found an isomorphism. We yield that mapping and backtrack to find other
    isomorphisms.

    As we visit more neighbors, the graph candidate nodes have to satisfy more structural
    restrictions. As described in the ISMAGS paper, [1]_, we store each set of structural
    restrictions separately as a set of possible candidate nodes rather than computing
    the intersection of that set with the known graph candidates for the subgraph node.
    We delay taking the intersection until that node is selected to be in the mapping.
    While choosing the node with fewest candidates, we avoid computing the intersection
    by using the size of the minimal set to be intersected rather than the size of the
    intersection. This may make the node ordering slightly worse via a savings of
    many intersections most of which are not ever needed.

    References
    ----------
    .. [1] M. Houbraken, S. Demeyer, T. Michoel, P. Audenaert, D. Colle,
       M. Pickavet, "The Index-Based Subgraph Matching Algorithm with General
       Symmetries (ISMAGS): Exploiting Symmetry for Faster Subgraph
       Enumeration", PLoS One 9(5): e97896, 2014.
       https://doi.org/10.1371/journal.pone.0097896
    .. [2] https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph
    .. [3] Hadi Katebi, Karem A. Sakallah and Igor L. Markov
       "Graph Symmetry Detection and Canonical Labeling: Differences and Synergies"
       in "Turing-100. The Alan Turing Centenary" Ed: A. Voronkov p. 181 -- 195, (2012).
       https://doi.org/10.29007/gzc1 https://arxiv.org/abs/1208.6271
    """
    graph: Incomplete
    subgraph: Incomplete

    def __init__(self, graph, subgraph, node_match=None, edge_match=None, cache=None) -> None:
        """
        Parameters
        ----------
        graph: networkx.Graph
        subgraph: networkx.Graph
        node_match: collections.abc.Callable or None
            Function used to determine whether two nodes are equivalent. Its
            signature should look like ``f(n1: dict, n2: dict) -> bool``, with
            `n1` and `n2` node property dicts. See also
            :func:`~networkx.algorithms.isomorphism.categorical_node_match` and
            friends.
            If `None`, all nodes are considered equal.
        edge_match: collections.abc.Callable or None
            Function used to determine whether two edges are equivalent. Its
            signature should look like ``f(e1: dict, e2: dict) -> bool``, with
            `e1` and `e2` edge property dicts. See also
            :func:`~networkx.algorithms.isomorphism.categorical_edge_match` and
            friends.
            If `None`, all edges are considered equal.
        cache: collections.abc.Mapping
            A cache used for caching graph symmetries.
        """
        ...
    def create_aligned_partitions(self, thing_matcher, sg_things, g_things):
        """
        Partitions of "things" (nodes or edges) from subgraph and graph
        based on function `thing_matcher`.

        Returns: sg_partition, g_partition, number_of_matched_parts

        The first `number_of_matched_parts` parts in each partition
        match in order, e.g. 2nd part matches other's 2nd part.
        Warning: nodes in parts after that have no matching nodes in the other graph.
        For morphisms those nodes can't appear in the mapping.
        """
        ...
    def find_isomorphisms(self, symmetry: bool = True) -> Generator[Incomplete, Incomplete, Incomplete]:
        """
        Find all subgraph isomorphisms between subgraph and graph

        Finds isomorphisms where :attr:`subgraph` <= :attr:`graph`.

        Parameters
        ----------
        symmetry: bool
            Whether symmetry should be taken into account. If False, found
            isomorphisms may be symmetrically equivalent.

        Yields
        ------
        dict
            The found isomorphism mappings of {graph_node: subgraph_node}.
        """
        ...
    def largest_common_subgraph(self, symmetry: bool = True) -> Generator[Incomplete, Incomplete]:
        """
        Find the largest common induced subgraphs between :attr:`subgraph` and
        :attr:`graph`.

        Parameters
        ----------
        symmetry: bool
            Whether symmetry should be taken into account. If False, found
            largest common subgraphs may be symmetrically equivalent.

        Yields
        ------
        dict
            The found isomorphism mappings of {graph_node: subgraph_node}.
        """
        ...
    def analyze_subgraph_symmetry(self) -> dict[Hashable, set[Hashable]]:
        """
        Find a minimal set of permutations and corresponding co-sets that
        describe the symmetry of ``self.subgraph``, given the node and edge
        equalities given by `node_partition` and `edge_colors`, respectively.

        Returns
        -------
        dict[collections.abc.Hashable, set[collections.abc.Hashable]]
            The found co-sets. The co-sets is a dictionary of
            ``{node key: set of node keys}``.
            Every key-value pair describes which ``values`` can be interchanged
            without changing nodes less than ``key``.
        """
        ...
    def is_isomorphic(self, symmetry: bool = False) -> bool:
        """
        Returns True if :attr:`graph` is isomorphic to :attr:`subgraph` and
        False otherwise.

        Returns
        -------
        bool
        """
        ...
    def subgraph_is_isomorphic(self, symmetry: bool = False) -> bool:
        """
        Returns True if a subgraph of :attr:`graph` is isomorphic to
        :attr:`subgraph` and False otherwise.

        Returns
        -------
        bool
        """
        ...
    def isomorphisms_iter(self, symmetry: bool = True) -> Generator[Incomplete, Incomplete]:
        """
        Does the same as :meth:`find_isomorphisms` if :attr:`graph` and
        :attr:`subgraph` have the same number of nodes.
        """
        ...
    def subgraph_isomorphisms_iter(self, symmetry: bool = True):
        """Alternative name for :meth:`find_isomorphisms`."""
        ...
