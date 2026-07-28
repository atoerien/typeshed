from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from typing import NamedTuple

__all__ = ["not_implemented_for", "open_file", "nodes_or_number", "np_random_state", "py_random_state", "argmap"]

def not_implemented_for(*graph_types) -> Callable[..., Incomplete]: ...
def open_file(path_arg: str | int, mode: str = "r") -> Callable[..., Incomplete]: ...
def nodes_or_number(which_args: str | int | Sequence[str | int]) -> Callable[..., Incomplete]: ...
def np_random_state(random_state_argument: str | int) -> Callable[..., Incomplete]: ...
def py_random_state(random_state_argument: str | int) -> Callable[..., Incomplete]: ...

class argmap:
    """
    A decorator to apply a map to arguments before calling the function

    This class provides a decorator that maps (transforms) arguments of the function
    before the function is called. Thus for example, we have similar code
    in many functions to determine whether an argument is the number of nodes
    to be created, or a list of nodes to be handled. The decorator provides
    the code to accept either -- transforming the indicated argument into a
    list of nodes before the actual function is called.

    This decorator class allows us to process single or multiple arguments.
    The arguments to be processed can be specified by string, naming the argument,
    or by index, specifying the item in the args list.

    Parameters
    ----------
    func : callable
        The function to apply to arguments

    *args : iterable of (int, str or tuple)
        A list of parameters, specified either as strings (their names), ints
        (numerical indices) or tuples, which may contain ints, strings, and
        (recursively) tuples. Each indicates which parameters the decorator
        should map. Tuples indicate that the map function takes (and returns)
        multiple parameters in the same order and nested structure as indicated
        here.

    try_finally : bool (default: False)
        When True, wrap the function call in a try-finally block with code
        for the finally block created by `func`. This is used when the map
        function constructs an object (like a file handle) that requires
        post-processing (like closing).

        Note: try_finally decorators cannot be used to decorate generator
        functions.

    Examples
    --------
    Most of these examples use `@argmap(...)` to apply the decorator to
    the function defined on the next line.
    In the NetworkX codebase however, `argmap` is used within a function to
    construct a decorator. That is, the decorator defines a mapping function
    and then uses `argmap` to build and return a decorated function.
    A simple example is a decorator that specifies which currency to report money.
    The decorator (named `convert_to`) would be used like::

        @convert_to("US_Dollars", "income")
        def show_me_the_money(name, income):
            print(f"{name} : {income}")

    And the code to create the decorator might be::

        def convert_to(currency, which_arg):
            def _convert(amount):
                if amount.currency != currency:
                    amount = amount.to_currency(currency)
                return amount

            return argmap(_convert, which_arg)

    Despite this common idiom for argmap, most of the following examples
    use the `@argmap(...)` idiom to save space.

    Here's an example use of argmap to sum the elements of two of the functions
    arguments. The decorated function::

        @argmap(sum, "xlist", "zlist")
        def foo(xlist, y, zlist):
            return xlist - y + zlist

    is syntactic sugar for::

        def foo(xlist, y, zlist):
            x = sum(xlist)
            z = sum(zlist)
            return x - y + z

    and is equivalent to (using argument indexes)::

        @argmap(sum, "xlist", 2)
        def foo(xlist, y, zlist):
            return xlist - y + zlist

    or::

        @argmap(sum, "zlist", 0)
        def foo(xlist, y, zlist):
            return xlist - y + zlist

    Transforming functions can be applied to multiple arguments, such as::

        def swap(x, y):
            return y, x

        # the 2-tuple tells argmap that the map `swap` has 2 inputs/outputs.
        @argmap(swap, ("a", "b")):
        def foo(a, b, c):
            return a / b * c

    is equivalent to::

        def foo(a, b, c):
            a, b = swap(a, b)
            return a / b * c

    More generally, the applied arguments can be nested tuples of strings or ints.
    The syntax `@argmap(some_func, ("a", ("b", "c")))` would expect `some_func` to
    accept 2 inputs with the second expected to be a 2-tuple. It should then return
    2 outputs with the second a 2-tuple. The returns values would replace input "a"
    "b" and "c" respectively. Similarly for `@argmap(some_func, (0, ("b", 2)))`.

    Also, note that an index larger than the number of named parameters is allowed
    for variadic functions. For example::

        def double(a):
            return 2 * a


        @argmap(double, 3)
        def overflow(a, *args):
            return a, args


        print(overflow(1, 2, 3, 4, 5, 6))  # output is 1, (2, 3, 8, 5, 6)

    **Try Finally**

    Additionally, this `argmap` class can be used to create a decorator that
    initiates a try...finally block. The decorator must be written to return
    both the transformed argument and a closing function.
    This feature was included to enable the `open_file` decorator which might
    need to close the file or not depending on whether it had to open that file.
    This feature uses the keyword-only `try_finally` argument to `@argmap`.

    For example this map opens a file and then makes sure it is closed::

        def open_file(fn):
            f = open(fn)
            return f, lambda: f.close()

    The decorator applies that to the function `foo`::

        @argmap(open_file, "file", try_finally=True)
        def foo(file):
            print(file.read())

    is syntactic sugar for::

        def foo(file):
            file, close_file = open_file(file)
            try:
                print(file.read())
            finally:
                close_file()

    and is equivalent to (using indexes)::

        @argmap(open_file, 0, try_finally=True)
        def foo(file):
            print(file.read())

    Here's an example of the try_finally feature used to create a decorator::

        def my_closing_decorator(which_arg):
            def _opener(path):
                if path is None:
                    path = open(path)
                    fclose = path.close
                else:
                    # assume `path` handles the closing
                    fclose = lambda: None
                return path, fclose

            return argmap(_opener, which_arg, try_finally=True)

    which can then be used as::

        @my_closing_decorator("file")
        def fancy_reader(file=None):
            # this code doesn't need to worry about closing the file
            print(file.read())

    Decorators with try_finally = True cannot be used with generator functions,
    because the `finally` block is evaluated before the generator is exhausted::

        @argmap(open_file, "file", try_finally=True)
        def file_to_lines(file):
            for line in file.readlines():
                yield line

    is equivalent to::

        def file_to_lines_wrapped(file):
            for line in file.readlines():
                yield line


        def file_to_lines_wrapper(file):
            try:
                file = open_file(file)
                return file_to_lines_wrapped(file)
            finally:
                file.close()

    which behaves similarly to::

        def file_to_lines_whoops(file):
            file = open_file(file)
            file.close()
            for line in file.readlines():
                yield line

    because the `finally` block of `file_to_lines_wrapper` is executed before
    the caller has a chance to exhaust the iterator.

    Notes
    -----
    An object of this class is callable and intended to be used when
    defining a decorator. Generally, a decorator takes a function as input
    and constructs a function as output. Specifically, an `argmap` object
    returns the input function decorated/wrapped so that specified arguments
    are mapped (transformed) to new values before the decorated function is called.

    As an overview, the argmap object returns a new function with all the
    dunder values of the original function (like `__doc__`, `__name__`, etc).
    Code for this decorated function is built based on the original function's
    signature. It starts by mapping the input arguments to potentially new
    values. Then it calls the decorated function with these new values in place
    of the indicated arguments that have been mapped. The return value of the
    original function is then returned. This new function is the function that
    is actually called by the user.

    Three additional features are provided.
        1) The code is lazily compiled. That is, the new function is returned
        as an object without the code compiled, but with all information
        needed so it can be compiled upon it's first invocation. This saves
        time on import at the cost of additional time on the first call of
        the function. Subsequent calls are then just as fast as normal.

        2) If the "try_finally" keyword-only argument is True, a try block
        follows each mapped argument, matched on the other side of the wrapped
        call, by a finally block closing that mapping.  We expect func to return
        a 2-tuple: the mapped value and a function to be called in the finally
        clause.  This feature was included so the `open_file` decorator could
        provide a file handle to the decorated function and close the file handle
        after the function call. It even keeps track of whether to close the file
        handle or not based on whether it had to open the file or the input was
        already open. So, the decorated function does not need to include any
        code to open or close files.

        3) The maps applied can process multiple arguments. For example,
        you could swap two arguments using a mapping, or transform
        them to their sum and their difference. This was included to allow
        a decorator in the `quality.py` module that checks that an input
        `partition` is a valid partition of the nodes of the input graph `G`.
        In this example, the map has inputs `(G, partition)`. After checking
        for a valid partition, the map either raises an exception or leaves
        the inputs unchanged. Thus many functions that make this check can
        use the decorator rather than copy the checking code into each function.
        More complicated nested argument structures are described below.

    The remaining notes describe the code structure and methods for this
    class in broad terms to aid in understanding how to use it.

    Instantiating an `argmap` object simply stores the mapping function and
    the input identifiers of which arguments to map. The resulting decorator
    is ready to use this map to decorate any function. Calling that object
    (`argmap.__call__`, but usually done via `@my_decorator`) a lazily
    compiled thin wrapper of the decorated function is constructed,
    wrapped with the necessary function dunder attributes like `__doc__`
    and `__name__`. That thinly wrapped function is returned as the
    decorated function. When that decorated function is called, the thin
    wrapper of code calls `argmap._lazy_compile` which compiles the decorated
    function (using `argmap.compile`) and replaces the code of the thin
    wrapper with the newly compiled code. This saves the compilation step
    every import of networkx, at the cost of compiling upon the first call
    to the decorated function.

    When the decorated function is compiled, the code is recursively assembled
    using the `argmap.assemble` method. The recursive nature is needed in
    case of nested decorators. The result of the assembly is a number of
    useful objects.

      sig : the function signature of the original decorated function as
          constructed by :func:`argmap.signature`. This is constructed
          using `inspect.signature` but enhanced with attribute
          strings `sig_def` and `sig_call`, and other information
          specific to mapping arguments of this function.
          This information is used to construct a string of code defining
          the new decorated function.

      wrapped_name : a unique internally used name constructed by argmap
          for the decorated function.

      functions : a dict of the functions used inside the code of this
          decorated function, to be used as `globals` in `exec`.
          This dict is recursively updated to allow for nested decorating.

      mapblock : code (as a list of strings) to map the incoming argument
          values to their mapped values.

      finallys : code (as a list of strings) to provide the possibly nested
          set of finally clauses if needed.

      mutable_args : a bool indicating whether the `sig.args` tuple should be
          converted to a list so mutation can occur.

    After this recursive assembly process, the `argmap.compile` method
    constructs code (as strings) to convert the tuple `sig.args` to a list
    if needed. It joins the defining code with appropriate indents and
    compiles the result.  Finally, this code is evaluated and the original
    wrapper's implementation is replaced with the compiled version (see
    `argmap._lazy_compile` for more details).

    Other `argmap` methods include `_name` and `_count` which allow internally
    generated names to be unique within a python session.
    The methods `_flatten` and `_indent` process the nested lists of strings
    into properly indented python code ready to be compiled.

    More complicated nested tuples of arguments also allowed though
    usually not used. For the simple 2 argument case, the argmap
    input ("a", "b") implies the mapping function will take 2 arguments
    and return a 2-tuple of mapped values. A more complicated example
    with argmap input `("a", ("b", "c"))` requires the mapping function
    take 2 inputs, with the second being a 2-tuple. It then must output
    the 3 mapped values in the same nested structure `(newa, (newb, newc))`.
    This level of generality is not often needed, but was convenient
    to implement when handling the multiple arguments.

    See Also
    --------
    not_implemented_for
    open_file
    nodes_or_number
    py_random_state
    networkx.algorithms.community.quality.require_partition
    """
    def __init__(self, func, *args, try_finally: bool = False) -> None: ...
    def __call__(self, f) -> Callable[..., Incomplete]: ...
    def compile(self, f: Callable[..., Incomplete]) -> Callable[..., Incomplete]: ...
    def assemble(self, f: Callable[..., Incomplete]): ...
    @classmethod
    def signature(cls, f: Callable[..., Incomplete]): ...

    class Signature(NamedTuple):
        """Signature(name, signature, def_sig, call_sig, names, n_positional, args, kwargs)"""
        name: Incomplete
        signature: Incomplete
        def_sig: Incomplete
        call_sig: Incomplete
        names: Incomplete
        n_positional: Incomplete
        args: Incomplete
        kwargs: Incomplete
