"""
Miscellaneous Helpers for NetworkX.

These are not imported into the base networkx namespace but
can be accessed, for example, as

>>> import networkx as nx
>>> nx.utils.make_list_of_ints({1, 2, 3})
[1, 2, 3]
>>> nx.utils.arbitrary_element({5, 1, 7})  # doctest: +SKIP
1
"""

import random
from types import ModuleType
from typing import TypeAlias

import numpy
from networkx.classes.graph import Graph, _Node

__all__ = [
    "flatten",
    "make_list_of_ints",
    "dict_to_numpy_array",
    "arbitrary_element",
    "pairwise",
    "groups",
    "create_random_state",
    "create_py_random_state",
    "PythonRandomInterface",
    "PythonRandomViaNumpyBits",
    "nodes_equal",
    "edges_equal",
    "graphs_equal",
    "_clear_cache",
]

_RandomNumberGenerator: TypeAlias = (
    ModuleType | random.Random | numpy.random.RandomState | numpy.random.Generator | PythonRandomInterface
)
_RandomState: TypeAlias = int | _RandomNumberGenerator | None

def flatten(obj, result=None):
    """Return flattened version of (possibly nested) iterable object."""
    ...
def make_list_of_ints(sequence):
    """
    Return list of ints from sequence of integral numbers.

    All elements of the sequence must satisfy int(element) == element
    or a ValueError is raised. Sequence is iterated through once.

    If sequence is a list, the non-int values are replaced with ints.
    So, no new list is created
    """
    ...
def dict_to_numpy_array(d, mapping=None):
    """
    Convert a dictionary of dictionaries to a numpy array
    with optional mapping.
    """
    ...
def arbitrary_element(iterable):
    """
    Returns an arbitrary element of `iterable` without removing it.

    This is most useful for "peeking" at an arbitrary element of a set,
    but can be used for any list, dictionary, etc., as well.

    Parameters
    ----------
    iterable : `abc.collections.Iterable` instance
        Any object that implements ``__iter__``, e.g. set, dict, list, tuple,
        etc.

    Returns
    -------
    The object that results from ``next(iter(iterable))``

    Raises
    ------
    ValueError
        If `iterable` is an iterator (because the current implementation of
        this function would consume an element from the iterator).

    Examples
    --------
    Arbitrary elements from common Iterable objects:

    >>> nx.utils.arbitrary_element([1, 2, 3])  # list
    1
    >>> nx.utils.arbitrary_element((1, 2, 3))  # tuple
    1
    >>> nx.utils.arbitrary_element({1, 2, 3})  # set
    1
    >>> d = {k: v for k, v in zip([1, 2, 3], [3, 2, 1])}
    >>> nx.utils.arbitrary_element(d)  # dict_keys
    1
    >>> nx.utils.arbitrary_element(d.values())  # dict values
    3

    `str` is also an Iterable:

    >>> nx.utils.arbitrary_element("hello")
    'h'

    :exc:`ValueError` is raised if `iterable` is an iterator:

    >>> iterator = iter([1, 2, 3])  # Iterator, *not* Iterable
    >>> nx.utils.arbitrary_element(iterator)
    Traceback (most recent call last):
        ...
    ValueError: cannot return an arbitrary item from an iterator

    Notes
    -----
    This function does not return a *random* element. If `iterable` is
    ordered, sequential calls will return the same value::

        >>> l = [1, 2, 3]
        >>> nx.utils.arbitrary_element(l)
        1
        >>> nx.utils.arbitrary_element(l)
        1
    """
    ...
def pairwise(iterable, cyclic: bool = False):
    """
    Return successive overlapping pairs taken from an input iterable.

    Parameters
    ----------
    iterable : iterable
        An iterable from which to generate pairs.

    cyclic : bool, optional (default=False)
        If `True`, a pair with the last and first items is included at the end.

    Returns
    -------
    iterator
        An iterator over successive overlapping pairs from the `iterable`.

    See Also
    --------
    itertools.pairwise

    Examples
    --------
    >>> list(nx.utils.pairwise([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    >>> list(nx.utils.pairwise([1, 2, 3, 4], cyclic=True))
    [(1, 2), (2, 3), (3, 4), (4, 1)]
    """
    ...
def groups(many_to_one):
    """
    Converts a many-to-one mapping into a one-to-many mapping.

    `many_to_one` must be a dictionary whose keys and values are all
    :term:`hashable`.

    The return value is a dictionary mapping values from `many_to_one`
    to sets of keys from `many_to_one` that have that value.

    Examples
    --------
    >>> from networkx.utils import groups
    >>> many_to_one = {"a": 1, "b": 1, "c": 2, "d": 3, "e": 3}
    >>> groups(many_to_one)  # doctest: +SKIP
    {1: {'a', 'b'}, 2: {'c'}, 3: {'e', 'd'}}
    """
    ...
def create_random_state(random_state=None):
    """
    Returns a numpy.random.RandomState or numpy.random.Generator instance
    depending on input.

    Parameters
    ----------
    random_state : int or NumPy RandomState or Generator instance, optional (default=None)
        If int, return a numpy.random.RandomState instance set with seed=int.
        if `numpy.random.RandomState` instance, return it.
        if `numpy.random.Generator` instance, return it.
        if None or numpy.random, return the global random number generator used
        by numpy.random.
    """
    ...

class PythonRandomViaNumpyBits(random.Random):
    """
    Provide the random.random algorithms using a numpy.random bit generator

    The intent is to allow people to contribute code that uses Python's random
    library, but still allow users to provide a single easily controlled random
    bit-stream for all work with NetworkX. This implementation is based on helpful
    comments and code from Robert Kern on NumPy's GitHub Issue #24458.

    This implementation supersedes that of `PythonRandomInterface` which rewrote
    methods to account for subtle differences in API between `random` and
    `numpy.random`. Instead this subclasses `random.Random` and overwrites
    the methods `random`, `getrandbits`, `getstate`, `setstate` and `seed`.
    It makes them use the rng values from an input numpy `RandomState` or `Generator`.
    Those few methods allow the rest of the `random.Random` methods to provide
    the API interface of `random.random` while using randomness generated by
    a numpy generator.
    """
    def __init__(self, rng: numpy.random.Generator | None = None) -> None: ...
    def getrandbits(self, k: int) -> int: ...

class PythonRandomInterface:
    """
    PythonRandomInterface is included for backward compatibility
    New code should use PythonRandomViaNumpyBits instead.
    """
    def __init__(self, rng=None) -> None: ...
    def random(self): ...
    def uniform(self, a, b): ...
    def randrange(self, a, b=None): ...
    def choice(self, seq): ...
    def gauss(self, mu, sigma): ...
    def shuffle(self, seq): ...
    def sample(self, seq, k): ...
    def randint(self, a, b): ...
    def expovariate(self, scale): ...
    def paretovariate(self, shape): ...

def create_py_random_state(random_state: _RandomState = None):
    """
    Returns a random.Random instance depending on input.

    Parameters
    ----------
    random_state : int or random number generator or None (default=None)
        - If int, return a `random.Random` instance set with seed=int.
        - If `random.Random` instance, return it.
        - If None or the `np.random` package, return the global random number
          generator used by `np.random`.
        - If an `np.random.Generator` instance, or the `np.random` package, or
          the global numpy random number generator, then return it.
          wrapped in a `PythonRandomViaNumpyBits` class.
        - If a `PythonRandomViaNumpyBits` instance, return it.
        - If a `PythonRandomInterface` instance, return it.
        - If a `np.random.RandomState` instance and not the global numpy default,
          return it wrapped in `PythonRandomInterface` for backward bit-stream
          matching with legacy code.

    Notes
    -----
    - A diagram intending to illustrate the relationships behind our support
      for numpy random numbers is called
      `NetworkX Numpy Random Numbers <https://excalidraw.com/#room=b5303f2b03d3af7ccc6a,e5ZDIWdWWCTTsg8OqoRvPA>`_.
    - More discussion about this support also appears in
      `gh-6869#comment <https://github.com/networkx/networkx/pull/6869#issuecomment-1944799534>`_.
    - Wrappers of numpy.random number generators allow them to mimic the Python random
      number generation algorithms. For example, Python can create arbitrarily large
      random ints, and the wrappers use Numpy bit-streams with CPython's random module
      to choose arbitrarily large random integers too.
    - We provide two wrapper classes:
      `PythonRandomViaNumpyBits` is usually what you want and is always used for
      `np.Generator` instances. But for users who need to recreate random numbers
      produced in NetworkX 3.2 or earlier, we maintain the `PythonRandomInterface`
      wrapper as well. We use it only used if passed a (non-default) `np.RandomState`
      instance pre-initialized from a seed. Otherwise the newer wrapper is used.
    """
    ...
def nodes_equal(nodes1, nodes2) -> bool:
    """
    Check if nodes are equal.

    Equality here means equal as Python objects.
    Node data must match if included.
    The order of nodes is not relevant.

    Parameters
    ----------
    nodes1, nodes2 : iterables of nodes, or (node, datadict) tuples

    Returns
    -------
    bool
        True if nodes are equal, False otherwise.
    """
    ...
def edges_equal(edges1, edges2, *, directed: bool = False) -> bool:
    """
    Return whether edgelists are equal.

    Equality here means equal as Python objects. Edge data must match
    if included. Ordering of edges in an edgelist is not relevant;
    ordering of nodes in an edge is only relevant if ``directed == True``.

    Parameters
    ----------
    edges1, edges2 : iterables of tuples
        Each tuple can be
        an edge tuple ``(u, v)``, or
        an edge tuple with data `dict` s ``(u, v, d)``, or
        an edge tuple with keys and data `dict` s ``(u, v, k, d)``.

    directed : bool, optional (default=False)
        If `True`, edgelists are treated as coming from directed
        graphs.

    Returns
    -------
    bool
        `True` if edgelists are equal, `False` otherwise.

    Examples
    --------
    >>> G1 = nx.complete_graph(3)
    >>> G2 = nx.cycle_graph(3)
    >>> edges_equal(G1.edges, G2.edges)
    True

    Edge order is not taken into account:

    >>> G1 = nx.Graph([(0, 1), (1, 2)])
    >>> G2 = nx.Graph([(1, 2), (0, 1)])
    >>> edges_equal(G1.edges, G2.edges)
    True

    The `directed` parameter controls whether edges are treated as
    coming from directed graphs.

    >>> DG1 = nx.DiGraph([(0, 1)])
    >>> DG2 = nx.DiGraph([(1, 0)])
    >>> edges_equal(DG1.edges, DG2.edges, directed=False)  # Not recommended.
    True
    >>> edges_equal(DG1.edges, DG2.edges, directed=True)
    False

    This function is meant to be used on edgelists (i.e. the output of a
    ``G.edges()`` call), and can give unexpected results on unprocessed
    lists of edges:

    >>> l1 = [(0, 1)]
    >>> l2 = [(0, 1), (1, 0)]
    >>> edges_equal(l1, l2)  # Not recommended.
    False
    >>> G1 = nx.Graph(l1)
    >>> G2 = nx.Graph(l2)
    >>> edges_equal(G1.edges, G2.edges)
    True
    >>> DG1 = nx.DiGraph(l1)
    >>> DG2 = nx.DiGraph(l2)
    >>> edges_equal(DG1.edges, DG2.edges, directed=True)
    False
    """
    ...
def graphs_equal(graph1, graph2) -> bool:
    """
    Check if graphs are equal.

    Equality here means equal as Python objects (not isomorphism).
    Node, edge and graph data must match.

    Parameters
    ----------
    graph1, graph2 : graph

    Returns
    -------
    bool
        True if graphs are equal, False otherwise.
    """
    ...
def _clear_cache(G: Graph[_Node]) -> None:
    """
    Clear the cache of a graph (currently stores converted graphs).

    Caching is controlled via ``nx.config.cache_converted_graphs`` configuration.
    """
    ...
