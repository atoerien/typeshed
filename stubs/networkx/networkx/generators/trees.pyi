"""
Functions for generating trees.

The functions sampling trees at random in this module come
in two variants: labeled and unlabeled. The labeled variants
sample from every possible tree with the given number of nodes
uniformly at random. The unlabeled variants sample from every
possible *isomorphism class* of trees with the given number
of nodes uniformly at random.

To understand the difference, consider the following example.
There are two isomorphism classes of trees with four nodes.
One is that of the path graph, the other is that of the
star graph. The unlabeled variant will return a line graph or
a star graph with probability 1/2.

The labeled variant will return the line graph
with probability 3/4 and the star graph with probability 1/4,
because there are more labeled variants of the line graph
than of the star graph. More precisely, the line graph has
an automorphism group of order 2, whereas the star graph has
an automorphism group of order 6, so the line graph has three
times as many labeled variants as the star graph, and thus
three more chances to be drawn.

Additionally, some functions in this module can sample rooted
trees and forests uniformly at random. A rooted tree is a tree
with a designated root node. A rooted forest is a disjoint union
of rooted trees.
"""

from _typeshed import Incomplete
from collections.abc import Iterable

from networkx.classes.graph import Graph
from networkx.utils.backends import _dispatchable

from ..classes.digraph import DiGraph

__all__ = [
    "prefix_tree",
    "prefix_tree_recursive",
    "random_labeled_tree",
    "random_labeled_rooted_tree",
    "random_labeled_rooted_forest",
    "random_unlabeled_tree",
    "random_unlabeled_rooted_tree",
    "random_unlabeled_rooted_forest",
]

@_dispatchable
def prefix_tree(paths: Iterable[Incomplete]) -> DiGraph[Incomplete]: ...
@_dispatchable
def prefix_tree_recursive(paths: Iterable[Incomplete]) -> DiGraph[Incomplete]: ...
@_dispatchable
def random_labeled_tree(n: int, *, seed=None): ...
@_dispatchable
def random_labeled_rooted_tree(n: int, *, seed=None) -> Graph[Incomplete]: ...
@_dispatchable
def random_unlabeled_rooted_tree(n: int, *, number_of_trees=None, seed=None) -> Incomplete | list[Incomplete]: ...
@_dispatchable
def random_labeled_rooted_forest(n: int, *, seed=None) -> Graph[Incomplete]: ...
@_dispatchable
def random_unlabeled_rooted_forest(n: int, *, q=None, number_of_forests=None, seed=None) -> Incomplete | list[Incomplete]: ...
@_dispatchable
def random_unlabeled_tree(n: int, *, number_of_trees=None, seed=None) -> Incomplete | list[Incomplete]: ...
