"""
:mod:`itertools` is full of great examples of Python generator
usage. However, there are still some critical gaps. ``iterutils``
fills many of those gaps with featureful, tested, and Pythonic
solutions.

Many of the functions below have two versions, one which
returns an iterator (denoted by the ``*_iter`` naming pattern), and a
shorter-named convenience form that returns a list. Some of the
following are based on examples in itertools docs.
"""

from _typeshed import Incomplete
from collections.abc import Generator

def is_iterable(obj) -> bool: ...
def is_scalar(obj) -> bool: ...
def is_collection(obj) -> bool: ...
def split(src, sep=None, maxsplit=None): ...
def split_iter(src, sep=None, maxsplit=None) -> Generator[Incomplete, None, Incomplete]: ...
def lstrip(iterable, strip_value=None): ...
def lstrip_iter(iterable, strip_value=None) -> Generator[Incomplete]: ...
def rstrip(iterable, strip_value=None): ...
def rstrip_iter(iterable, strip_value=None) -> Generator[Incomplete]: ...
def strip(iterable, strip_value=None): ...
def strip_iter(iterable, strip_value=None): ...
def chunked(src, size, count=None, **kw): ...
def chunked_iter(src, size, **kw) -> Generator[Incomplete, None, Incomplete]: ...
def chunk_ranges(
    input_size: int, chunk_size: int, input_offset: int = 0, overlap_size: int = 0, align: bool = False
) -> Generator[tuple[int, int]]: ...
def pairwise(src, end=...): ...
def pairwise_iter(src, end=...): ...
def windowed(src, size, fill=...): ...
def windowed_iter(src, size, fill=...): ...
def xfrange(stop, start=None, step: float = 1.0) -> Generator[Incomplete]: ...
def frange(stop, start=None, step: float = 1.0): ...
def backoff(start, stop, count=None, factor: float = 2.0, jitter: bool = False): ...
def backoff_iter(start, stop, count=None, factor: float = 2.0, jitter: bool = False) -> Generator[Incomplete]: ...
def bucketize(src, key=..., value_transform=None, key_filter=None): ...
def partition(src, key=...): ...
def unique(src, key=None): ...
def unique_iter(src, key=None) -> Generator[Incomplete, None, Incomplete]: ...
def redundant(src, key=None, groups: bool = False): ...
def one(src, default=None, key=None): ...
def first(iterable, default=None, key=None): ...
def flatten_iter(iterable) -> Generator[Incomplete]: ...
def flatten(iterable): ...
def same(iterable, ref=...): ...
def default_visit(path, key, value): ...
def default_enter(path, key, value): ...
def default_exit(path, key, old_parent, new_parent, new_items): ...
def remap(root, visit=..., enter=..., exit=..., **kwargs):
    """
    The remap ("recursive map") function is used to traverse and
    transform nested structures. Lists, tuples, sets, and dictionaries
    are just a few of the data structures nested into heterogeneous
    tree-like structures that are so common in programming.
    Unfortunately, Python's built-in ways to manipulate collections
    are almost all flat. List comprehensions may be fast and succinct,
    but they do not recurse, making it tedious to apply quick changes
    or complex transforms to real-world data.

    remap goes where list comprehensions cannot.

    Here's an example of removing all Nones from some data:

    >>> from pprint import pprint
    >>> reviews = {'Star Trek': {'TNG': 10, 'DS9': 8.5, 'ENT': None},
    ...            'Babylon 5': 6, 'Dr. Who': None}
    >>> pprint(remap(reviews, lambda p, k, v: v is not None))
    {'Babylon 5': 6, 'Star Trek': {'DS9': 8.5, 'TNG': 10}}

    Notice how both Nones have been removed despite the nesting in the
    dictionary. Not bad for a one-liner, and that's just the beginning.
    See `this remap cookbook`_ for more delicious recipes.

    .. _this remap cookbook: http://sedimental.org/remap.html

    remap takes four main arguments: the object to traverse and three
    optional callables which determine how the remapped object will be
    created.

    Args:

        root: The target object to traverse. By default, remap
            supports iterables like :class:`list`, :class:`tuple`,
            :class:`dict`, and :class:`set`, but any object traversable by
            *enter* will work.
        visit (callable): This function is called on every item in
            *root*. It must accept three positional arguments, *path*,
            *key*, and *value*. *path* is simply a tuple of parents'
            keys. *visit* should return the new key-value pair. It may
            also return ``True`` as shorthand to keep the old item
            unmodified, or ``False`` to drop the item from the new
            structure. *visit* is called after *enter*, on the new parent.

            The *visit* function is called for every item in root,
            including duplicate items. For traversable values, it is
            called on the new parent object, after all its children
            have been visited. The default visit behavior simply
            returns the key-value pair unmodified.
        enter (callable): This function controls which items in *root*
            are traversed. It accepts the same arguments as *visit*: the
            path, the key, and the value of the current item. It returns a
            pair of the blank new parent, and an iterator over the items
            which should be visited. If ``False`` is returned instead of
            an iterator, the value will not be traversed.

            The *enter* function is only called once per unique value. The
            default enter behavior support mappings, sequences, and
            sets. Strings and all other iterables will not be traversed.
        exit (callable): This function determines how to handle items
            once they have been visited. It gets the same three
            arguments as the other functions -- *path*, *key*, *value*
            -- plus two more: the blank new parent object returned
            from *enter*, and a list of the new items, as remapped by
            *visit*.

            Like *enter*, the *exit* function is only called once per
            unique value. The default exit behavior is to simply add
            all new items to the new parent, e.g., using
            :meth:`list.extend` and :meth:`dict.update` to add to the
            new parent. Immutable objects, such as a :class:`tuple` or
            :class:`namedtuple`, must be recreated from scratch, but
            use the same type as the new parent passed back from the
            *enter* function.
        reraise_visit (bool): A pragmatic convenience for the *visit*
            callable. When set to ``False``, remap ignores any errors
            raised by the *visit* callback. Items causing exceptions
            are kept. See examples for more details.
        trace (bool): Pass ``trace=True`` to print out the entire
            traversal. Or pass a tuple of ``'visit'``, ``'enter'``,
            or ``'exit'`` to print only the selected events.

    remap is designed to cover the majority of cases with just the
    *visit* callable. While passing in multiple callables is very
    empowering, remap is designed so very few cases should require
    passing more than one function.

    When passing *enter* and *exit*, it's common and easiest to build
    on the default behavior. Simply add ``from boltons.iterutils import
    default_enter`` (or ``default_exit``), and have your enter/exit
    function call the default behavior before or after your custom
    logic. See `this example`_.

    Duplicate and self-referential objects (aka reference loops) are
    automatically handled internally, `as shown here`_.

    .. _this example: http://sedimental.org/remap.html#sort_all_lists
    .. _as shown here: http://sedimental.org/remap.html#corner_cases
    """
    ...

class PathAccessError(KeyError, IndexError, TypeError):
    """
    An amalgamation of KeyError, IndexError, and TypeError,
    representing what can occur when looking up a path in a nested
    object.
    """
    exc: Incomplete
    seg: Incomplete
    path: Incomplete
    def __init__(self, exc, seg, path) -> None: ...

def get_path(root, path, default=...):
    """
    Retrieve a value from a nested object via a tuple representing the
    lookup path.

    >>> root = {'a': {'b': {'c': [[1], [2], [3]]}}}
    >>> get_path(root, ('a', 'b', 'c', 2, 0))
    3

    The path tuple format is intentionally consistent with that of
    :func:`remap`, but a single dotted string can also be passed.

    One of get_path's chief aims is improved error messaging. EAFP is
    great, but the error messages are not.

    For instance, ``root['a']['b']['c'][2][1]`` gives back
    ``IndexError: list index out of range``

    What went out of range where? get_path currently raises
    ``PathAccessError: could not access 2 from path ('a', 'b', 'c', 2,
    1), got error: IndexError('list index out of range',)``, a
    subclass of IndexError and KeyError.

    You can also pass a default that covers the entire operation,
    should the lookup fail at any level.

    Args:
       root: The target nesting of dictionaries, lists, or other
          objects supporting ``__getitem__``.
       path (tuple): A sequence of strings and integers to be successively
          looked up within *root*. A dot-separated (``a.b``) string may 
          also be passed.
       default: The value to be returned should any
          ``PathAccessError`` exceptions be raised.
    """
    ...
def research(root, query=..., reraise: bool = False, enter=...):
    """
    The :func:`research` function uses :func:`remap` to recurse over
    any data nested in *root*, and find values which match a given
    criterion, specified by the *query* callable.

    Results are returned as a list of ``(path, value)`` pairs. The
    paths are tuples in the same format accepted by
    :func:`get_path`. This can be useful for comparing values nested
    in two or more different structures.

    Here's a simple example that finds all integers:

    >>> root = {'a': {'b': 1, 'c': (2, 'd', 3)}, 'e': None}
    >>> res = research(root, query=lambda p, k, v: isinstance(v, int))
    >>> print(sorted(res))
    [(('a', 'b'), 1), (('a', 'c', 0), 2), (('a', 'c', 2), 3)]

    Note how *query* follows the same, familiar ``path, key, value``
    signature as the ``visit`` and ``enter`` functions on
    :func:`remap`, and returns a :class:`bool`.

    Args:
       root: The target object to search. Supports the same types of
          objects as :func:`remap`, including :class:`list`,
          :class:`tuple`, :class:`dict`, and :class:`set`.
       query (callable): The function called on every object to
          determine whether to include it in the search results. The
          callable must accept three arguments, *path*, *key*, and
          *value*, commonly abbreviated *p*, *k*, and *v*, same as
          *enter* and *visit* from :func:`remap`.
       reraise (bool): Whether to reraise exceptions raised by *query*
          or to simply drop the result that caused the error.


    With :func:`research` it's easy to inspect the details of a data
    structure, like finding values that are at a certain depth (using
    ``len(p)``) and much more. If more advanced functionality is
    needed, check out the code and make your own :func:`remap`
    wrapper, and consider `submitting a patch`_!

    .. _submitting a patch: https://github.com/mahmoud/boltons/pulls
    """
    ...

class GUIDerator:
    """
    The GUIDerator is an iterator that yields a globally-unique
    identifier (GUID) on every iteration. The GUIDs produced are
    hexadecimal strings.

    Testing shows it to be around 12x faster than the uuid module. By
    default it is also more compact, partly due to its default 96-bit
    (24-hexdigit) length. 96 bits of randomness means that there is a
    1 in 2 ^ 32 chance of collision after 2 ^ 64 iterations. If more
    or less uniqueness is desired, the *size* argument can be adjusted
    accordingly.

    Args:
        size (int): character length of the GUID, defaults to 24. Lengths
                    between 20 and 36 are considered valid.

    The GUIDerator has built-in fork protection that causes it to
    detect a fork on next iteration and reseed accordingly.
    """
    size: Incomplete
    count: Incomplete
    def __init__(self, size: int = 24) -> None: ...
    pid: Incomplete
    salt: Incomplete
    def reseed(self) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...
    next: Incomplete

class SequentialGUIDerator(GUIDerator):
    """
    Much like the standard GUIDerator, the SequentialGUIDerator is an
    iterator that yields a globally-unique identifier (GUID) on every
    iteration. The GUIDs produced are hexadecimal strings.

    The SequentialGUIDerator differs in that it picks a starting GUID
    value and increments every iteration. This yields GUIDs which are
    of course unique, but also ordered and lexicographically sortable.

    The SequentialGUIDerator is around 50% faster than the normal
    GUIDerator, making it almost 20x as fast as the built-in uuid
    module. By default it is also more compact, partly due to its
    96-bit (24-hexdigit) default length. 96 bits of randomness means that
    there is a 1 in 2 ^ 32 chance of collision after 2 ^ 64
    iterations. If more or less uniqueness is desired, the *size*
    argument can be adjusted accordingly.

    Args:
        size (int): character length of the GUID, defaults to 24.

    Note that with SequentialGUIDerator there is a chance of GUIDs
    growing larger than the size configured. The SequentialGUIDerator
    has built-in fork protection that causes it to detect a fork on
    next iteration and reseed accordingly.
    """
    start: Incomplete
    def reseed(self) -> None: ...
    def __next__(self): ...
    next: Incomplete

guid_iter: Incomplete
seq_guid_iter: Incomplete

def soft_sorted(iterable, first=None, last=None, key=None, reverse: bool = False):
    """
    For when you care about the order of some elements, but not about
    others.

    Use this to float to the top and/or sink to the bottom a specific
    ordering, while sorting the rest of the elements according to
    normal :func:`sorted` rules.

    >>> soft_sorted(['two', 'b', 'one', 'a'], first=['one', 'two'])
    ['one', 'two', 'a', 'b']
    >>> soft_sorted(range(7), first=[6, 15], last=[2, 4], reverse=True)
    [6, 5, 3, 1, 0, 2, 4]
    >>> import string
    >>> ''.join(soft_sorted(string.hexdigits, first='za1', last='b', key=str.lower))
    'aA1023456789cCdDeEfFbB'

    Args:
       iterable (list): A list or other iterable to sort.
       first (list): A sequence to enforce for elements which should
          appear at the beginning of the returned list.
       last (list): A sequence to enforce for elements which should
          appear at the end of the returned list.
       key (callable): Callable used to generate a comparable key for
          each item to be sorted, same as the key in
          :func:`sorted`. Note that entries in *first* and *last*
          should be the keys for the items. Defaults to
          passthrough/the identity function.
       reverse (bool): Whether or not elements not explicitly ordered
          by *first* and *last* should be in reverse order or not.

    Returns a new list in sorted order.
    """
    ...
def untyped_sorted(iterable, key=None, reverse: bool = False):
    """
    A version of :func:`sorted` which will happily sort an iterable of
    heterogeneous types and return a new list, similar to legacy Python's
    behavior.

    >>> untyped_sorted(['abc', 2.0, 1, 2, 'def'])
    [1, 2.0, 2, 'abc', 'def']

    Note how mutually orderable types are sorted as expected, as in
    the case of the integers and floats above.

    .. note::

       Results may vary across Python versions and builds, but the
       function will produce a sorted list, except in the case of
       explicitly unorderable objects.
    """
    ...
