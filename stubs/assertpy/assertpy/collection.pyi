from _typeshed import SupportsRichComparison
from collections.abc import Callable
from typing import Any, Generic, Literal, TypeVar, overload
from typing_extensions import Self

__tracebackhide__: bool

_V = TypeVar("_V", default=Any)

class CollectionMixin(Generic[_V]):
    def is_iterable(self) -> Self: ...
    def is_not_iterable(self) -> Self: ...
    def is_subset_of(self, *supersets: _V) -> Self: ...

    @overload
    def is_sorted(self, key: Callable[[_V], SupportsRichComparison] = ..., reverse: Literal[False] = False) -> Self:
        """
        Asserts that val is iterable and is sorted.

        Args:
            key (function): the one-arg function to extract the sort comparison key.  Defaults to
                ``lambda x: x`` to just compare items directly.
            reverse (bool): if ``True``, then comparison key is reversed.  Defaults to ``False``.

        Examples:
            Usage::

                assert_that(['a', 'b', 'c']).is_sorted()
                assert_that((1, 2, 3)).is_sorted()

                # with a key function
                assert_that('aBc').is_sorted(key=str.lower)

                # reverse order
                assert_that(['c', 'b', 'a']).is_sorted(reverse=True)
                assert_that((3, 2, 1)).is_sorted(reverse=True)

                assert_that((1, 2, 3, 4, -5, 6)).is_sorted()  # fails
                # Expected <(1, 2, 3, 4, -5, 6)> to be sorted, but subset <4, -5> at index 3 is not.

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** sorted
        """
        ...
    @overload
    def is_sorted(self, *, reverse: Literal[True]) -> Self:
        """
        Asserts that val is iterable and is sorted.

        Args:
            key (function): the one-arg function to extract the sort comparison key.  Defaults to
                ``lambda x: x`` to just compare items directly.
            reverse (bool): if ``True``, then comparison key is reversed.  Defaults to ``False``.

        Examples:
            Usage::

                assert_that(['a', 'b', 'c']).is_sorted()
                assert_that((1, 2, 3)).is_sorted()

                # with a key function
                assert_that('aBc').is_sorted(key=str.lower)

                # reverse order
                assert_that(['c', 'b', 'a']).is_sorted(reverse=True)
                assert_that((3, 2, 1)).is_sorted(reverse=True)

                assert_that((1, 2, 3, 4, -5, 6)).is_sorted()  # fails
                # Expected <(1, 2, 3, 4, -5, 6)> to be sorted, but subset <4, -5> at index 3 is not.

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** sorted
        """
        ...
    @overload
    def is_sorted(self, key: Callable[[_V], SupportsRichComparison], reverse: Literal[True]) -> Self:
        """
        Asserts that val is iterable and is sorted.

        Args:
            key (function): the one-arg function to extract the sort comparison key.  Defaults to
                ``lambda x: x`` to just compare items directly.
            reverse (bool): if ``True``, then comparison key is reversed.  Defaults to ``False``.

        Examples:
            Usage::

                assert_that(['a', 'b', 'c']).is_sorted()
                assert_that((1, 2, 3)).is_sorted()

                # with a key function
                assert_that('aBc').is_sorted(key=str.lower)

                # reverse order
                assert_that(['c', 'b', 'a']).is_sorted(reverse=True)
                assert_that((3, 2, 1)).is_sorted(reverse=True)

                assert_that((1, 2, 3, 4, -5, 6)).is_sorted()  # fails
                # Expected <(1, 2, 3, 4, -5, 6)> to be sorted, but subset <4, -5> at index 3 is not.

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** sorted
        """
        ...
