"""Provides functions for computing minors of a graph."""

from _typeshed import Incomplete
from collections.abc import Callable, Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["contracted_edge", "contracted_nodes", "equivalence_classes", "identified_nodes", "quotient_graph"]

@_dispatchable
def equivalence_classes(iterable: Iterable[_Node], relation: Callable[[_Node, _Node], bool]) -> set[frozenset[_Node]]:
    """
    Returns equivalence classes of `relation` when applied to `iterable`.

    The equivalence classes, or blocks, consist of objects from `iterable`
    which are all equivalent. They are defined to be equivalent if the
    `relation` function returns `True` when passed any two objects from that
    class, and `False` otherwise. To define an equivalence relation the
    function must be reflexive, symmetric and transitive.

    Parameters
    ----------
    iterable : list, tuple, or set
        An iterable of elements/nodes.

    relation : function
        A Boolean-valued function that implements an equivalence relation
        (reflexive, symmetric, transitive binary relation) on the elements
        of `iterable` - it must take two elements and return `True` if
        they are related, or `False` if not.

    Returns
    -------
    set of frozensets
        A set of frozensets representing the partition induced by the equivalence
        relation function `relation` on the elements of `iterable`. Each
        member set in the return set represents an equivalence class, or
        block, of the partition.

        Duplicate elements will be ignored so it makes the most sense for
        `iterable` to be a :class:`set`.

    Notes
    -----
    This function does not check that `relation` represents an equivalence
    relation. You can check that your equivalence classes provide a partition
    using `is_partition`.

    Examples
    --------
    Let `X` be the set of integers from `0` to `9`, and consider an equivalence
    relation `R` on `X` of congruence modulo `3`: this means that two integers
    `x` and `y` in `X` are equivalent under `R` if they leave the same
    remainder when divided by `3`, i.e. `(x - y) mod 3 = 0`.

    The equivalence classes of this relation are `{0, 3, 6, 9}`, `{1, 4, 7}`,
    `{2, 5, 8}`: `0`, `3`, `6`, `9` are all divisible by `3` and leave zero
    remainder; `1`, `4`, `7` leave remainder `1`; while `2`, `5` and `8` leave
    remainder `2`. We can see this by calling `equivalence_classes` with
    `X` and a function implementation of `R`.

    >>> X = set(range(10))
    >>> def mod3(x, y):
    ...     return (x - y) % 3 == 0
    >>> equivalence_classes(X, mod3)  # doctest: +SKIP
    {frozenset({1, 4, 7}), frozenset({8, 2, 5}), frozenset({0, 9, 3, 6})}
    """
    ...
@_dispatchable
def quotient_graph(
    G: Graph[_Node],
    partition: Callable[..., Incomplete] | dict[Incomplete, Incomplete] | list[set[Incomplete]],
    edge_relation: Callable[..., Incomplete] | None = None,
    node_data: Callable[..., Incomplete] | None = None,
    edge_data: Callable[..., Incomplete] | None = None,
    weight: str | None = "weight",
    relabel: bool = False,
    create_using: Graph[_Node] | type[Graph[_Node]] | None = None,
) -> Graph[Incomplete]: ...
@_dispatchable
def contracted_nodes(
    G: Graph[_Node], u, v, self_loops: bool = True, copy: bool = True, *, store_contraction_as: str | None = "contraction"
) -> Graph[Incomplete]: ...

identified_nodes = contracted_nodes

@_dispatchable
def contracted_edge(
    G: Graph[_Node],
    edge: tuple[Incomplete],
    self_loops: bool = True,
    copy: bool = True,
    *,
    store_contraction_as: str | None = "contraction",
) -> Graph[Incomplete]: ...
