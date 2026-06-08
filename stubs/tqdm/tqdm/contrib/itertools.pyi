"""Thin wrappers around `itertools`."""

from collections.abc import Callable, Generator, Iterable
from typing import Any, TypeVar

from ..std import tqdm as std_tqdm

__all__ = ["chain", "product", "permutations", "combinations", "combinations_with_replacement", "batched"]

_T = TypeVar("_T")

# In all functions below, kwargs are forwarded to tqdm_class.
def chain(
    *iterables: Iterable[_T], total: int | None = None, tqdm_class: Callable[..., std_tqdm[_T]] = ..., **kwargs: Any
) -> std_tqdm[_T]:
    """Equivalent of `itertools.chain`."""
    ...
def product(
    *iterables: Iterable[_T],
    repeat: int = 1,
    total: int | None = None,
    tqdm_class: Callable[..., std_tqdm[tuple[_T, ...]]] = ...,
    **kwargs: Any,
) -> Generator[tuple[_T, ...]]:
    """Equivalent of `itertools.product`."""
    ...
def permutations(
    iterable: Iterable[_T],
    r: int | None = None,
    total: int | None = None,
    tqdm_class: Callable[..., std_tqdm[tuple[_T, ...]]] = ...,
    **kwargs: Any,
) -> std_tqdm[tuple[_T, ...]]:
    """Equivalent of `itertools.permutations`."""
    ...
def combinations(
    iterable: Iterable[_T],
    r: int,
    total: int | None = None,
    tqdm_class: Callable[..., std_tqdm[tuple[_T, ...]]] = ...,
    **kwargs: Any,
) -> std_tqdm[tuple[_T, ...]]:
    """Equivalent of `itertools.combinations`."""
    ...
def combinations_with_replacement(
    iterable: Iterable[_T],
    r: int,
    total: int | None = None,
    tqdm_class: Callable[..., std_tqdm[tuple[_T, ...]]] = ...,
    **kwargs: Any,
) -> std_tqdm[tuple[_T, ...]]:
    """Equivalent of `itertools.combinations_with_replacement`."""
    ...
def batched(
    iterable: Iterable[_T],
    n: int,
    total: int | None = None,
    tqdm_class: Callable[..., std_tqdm[tuple[_T, ...]]] = ...,
    **kwargs: Any,
) -> std_tqdm[tuple[_T, ...]]:
    """Equivalent of `itertools.batched`."""
    ...
