"""Thin wrappers around `concurrent.futures`."""

import sys
from _typeshed import SupportsWrite
from collections.abc import Callable, Generator, Iterable, Mapping
from contextlib import contextmanager
from multiprocessing.context import BaseContext
from typing import Any, TypedDict, TypeVar, overload, type_check_only
from typing_extensions import Unpack

from ..std import tqdm

__all__ = ["thread_map", "process_map", "interpreter_map"]

_R = TypeVar("_R")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")

@type_check_only
class _TqdmCommonKwargs(TypedDict, total=False):
    # Concurrent-specific parameters
    tqdm_class: type[tqdm[object]]
    max_workers: int | None
    chunksize: int
    # Standard tqdm parameters
    desc: str | None
    total: float | None
    leave: bool | None
    file: SupportsWrite[str] | None
    ncols: int | None
    mininterval: float
    maxinterval: float
    miniters: float | None
    ascii: bool | str | None
    disable: bool | None
    unit: str
    unit_scale: bool | float
    dynamic_ncols: bool
    smoothing: float
    bar_format: str | None
    initial: float
    position: int | None
    postfix: Mapping[str, object] | str | None
    unit_divisor: float
    write_bytes: bool | None
    lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None
    nrows: int | None
    colour: str | None
    delay: float | None

# TODO: refactor this, when `TypedDict` will support conditional fields
if sys.version_info >= (3, 14):
    @type_check_only
    class _TqdmKwargs(_TqdmCommonKwargs):
        buffersize: int | None

else:
    _TqdmKwargs = _TqdmCommonKwargs

@type_check_only
class _TqdmProcessKwargs(_TqdmKwargs):
    mp_context: BaseContext | None
    max_tasks_per_child: int | None

@type_check_only
class _TqdmThreadKwargs(_TqdmKwargs):
    thread_name_prefix: str | None
    # Not techically for threading, but just a signature difference:
    lock_name: str

@contextmanager
def ensure_lock(tqdm_class: type[tqdm[object]], lock_name: str = "", lock=None) -> Generator[None]:
    """get (create if necessary) and then restore `tqdm_class`'s lock"""
    ...

@overload
def thread_map(fn: Callable[[_T1], _R], iter1: Iterable[_T1], **tqdm_kwargs: Unpack[_TqdmThreadKwargs]) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...
@overload
def thread_map(
    fn: Callable[[_T1, _T2], _R], iter1: Iterable[_T1], iter2: Iterable[_T2], /, **tqdm_kwargs: Unpack[_TqdmThreadKwargs]
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...
@overload
def thread_map(
    fn: Callable[[_T1, _T2, _T3], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...
@overload
def thread_map(
    fn: Callable[[_T1, _T2, _T3, _T4], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...
@overload
def thread_map(
    fn: Callable[[_T1, _T2, _T3, _T4, _T5], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    iter5: Iterable[_T5],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...
@overload
def thread_map(
    fn: Callable[..., _R],
    iter1: Iterable[Any],
    iter2: Iterable[Any],
    iter3: Iterable[Any],
    iter4: Iterable[Any],
    iter5: Iterable[Any],
    iter6: Iterable[Any],
    *iterables: Iterable[Any],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ThreadPoolExecutor`.
    thread_name_prefix  : str, optional
        Passed to `concurrent.futures.ThreadPoolExecutor` [default: ''].
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: ''].
    """
    ...

@overload
def process_map(
    fn: Callable[[_T1], _R], iter1: Iterable[_T1], *, lock_name: str = "mp_lock", **tqdm_kwargs: Unpack[_TqdmProcessKwargs]
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...
@overload
def process_map(
    fn: Callable[[_T1, _T2], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    *,
    lock_name: str = "mp_lock",
    **tqdm_kwargs: Unpack[_TqdmProcessKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...
@overload
def process_map(
    fn: Callable[[_T1, _T2, _T3], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    *,
    lock_name: str = "mp_lock",
    **tqdm_kwargs: Unpack[_TqdmProcessKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...
@overload
def process_map(
    fn: Callable[[_T1, _T2, _T3, _T4], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    *,
    lock_name: str = "mp_lock",
    **tqdm_kwargs: Unpack[_TqdmProcessKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...
@overload
def process_map(
    fn: Callable[[_T1, _T2, _T3, _T4, _T5], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    iter5: Iterable[_T5],
    *,
    lock_name: str = "mp_lock",
    **tqdm_kwargs: Unpack[_TqdmProcessKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...
@overload
def process_map(
    fn: Callable[..., _R],
    iter1: Iterable[Any],
    iter2: Iterable[Any],
    iter3: Iterable[Any],
    iter4: Iterable[Any],
    iter5: Iterable[Any],
    iter6: Iterable[Any],
    *iterables: Iterable[Any],
    lock_name: str = "mp_lock",
    **tqdm_kwargs: Unpack[_TqdmProcessKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to `concurrent.futures.ProcessPoolExecutor`.
    timeout  : int or float, optional
        Seconds to wait before raising `TimeoutError` if `__next__` is called and the
        result isn't available. [default: None].
    chunksize  : int, optional
        Approximate size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    buffersize  : int, optional
        Requires Python>=3.14 [default: None].
    max_tasks_per_child  : int, optional
        Maximum number of tasks a worker process can complete before being replaced
        with a new process; passed to `concurrent.futures.ProcessPoolExecutor`.
    mp_context  : multiprocessing.BaseContext, optional
        Multiprocessing context to use, e.g. `multiprocessing.get_context('fork')`.
    lock_name  : str, optional
        Member of `tqdm_class.get_lock()` to use [default: mp_lock].
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    smoothing  : float, optional
        Passed to `tqdm_class`; the [default: 0] is average (due to erratic update frequency).
    """
    ...

@overload
def interpreter_map(fn: Callable[[_T1], _R], iter1: Iterable[_T1], **tqdm_kwargs: Unpack[_TqdmThreadKwargs]) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
@overload
def interpreter_map(
    fn: Callable[[_T1, _T2], _R], iter1: Iterable[_T1], iter2: Iterable[_T2], /, **tqdm_kwargs: Unpack[_TqdmThreadKwargs]
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
@overload
def interpreter_map(
    fn: Callable[[_T1, _T2, _T3], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
@overload
def interpreter_map(
    fn: Callable[[_T1, _T2, _T3, _T4], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
@overload
def interpreter_map(
    fn: Callable[[_T1, _T2, _T3, _T4, _T5], _R],
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    iter3: Iterable[_T3],
    iter4: Iterable[_T4],
    iter5: Iterable[_T5],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
@overload
def interpreter_map(
    fn: Callable[..., _R],
    iter1: Iterable[Any],
    iter2: Iterable[Any],
    iter3: Iterable[Any],
    iter4: Iterable[Any],
    iter5: Iterable[Any],
    iter6: Iterable[Any],
    *iterables: Iterable[Any],
    **tqdm_kwargs: Unpack[_TqdmThreadKwargs],
) -> list[_R]:
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.InterpreterPoolExecutor` (Python 3.14+).

    Parameters
    ----------
    Same as `thread_map`.

    Notes
    -----
    `fn`, its arguments, and its return values must be pickleable.
    Worker progress bars using the same `tqdm_class` share a cross-interpreter write lock.
    """
    ...
