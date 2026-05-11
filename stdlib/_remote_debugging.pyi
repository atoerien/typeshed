from _typeshed import StrOrBytesPath, structseq
from collections.abc import Callable
from typing import Final, TypeAlias, final
from typing_extensions import Self

_Location: TypeAlias = tuple[int, int, int, int] | LocationInfo | None
_Frame: TypeAlias = tuple[str, _Location, str, int | None] | FrameInfo
_Stats: TypeAlias = dict[str, int | float]

PROCESS_VM_READV_SUPPORTED: Final[int]
THREAD_STATUS_GIL_REQUESTED: Final[int]
THREAD_STATUS_HAS_EXCEPTION: Final[int]
THREAD_STATUS_HAS_GIL: Final[int]
THREAD_STATUS_MAIN_THREAD: Final[int]
THREAD_STATUS_ON_CPU: Final[int]
THREAD_STATUS_UNKNOWN: Final[int]

@final
class LocationInfo(structseq[int], tuple[int, int, int, int]):
    __match_args__: Final = ("lineno", "end_lineno", "col_offset", "end_col_offset")
    @property
    def lineno(self) -> int: ...
    @property
    def end_lineno(self) -> int: ...
    @property
    def col_offset(self) -> int: ...
    @property
    def end_col_offset(self) -> int: ...

@final
class FrameInfo(structseq[object], tuple[str, _Location, str, int | None]):
    """Information about a frame"""
    __match_args__: Final = ("filename", "location", "funcname", "opcode")
    @property
    def filename(self) -> str:
        """Source code filename"""
        ...
    @property
    def location(self) -> _Location: ...
    @property
    def funcname(self) -> str:
        """Function name"""
        ...
    @property
    def opcode(self) -> int | None: ...

@final
class CoroInfo(structseq[object], tuple[list[_Frame], int | str]):
    """Information about a coroutine"""
    __match_args__: Final = ("call_stack", "task_name")
    @property
    def call_stack(self) -> list[_Frame]:
        """Coroutine call stack"""
        ...
    @property
    def task_name(self) -> int | str:
        """Task name"""
        ...

@final
class TaskInfo(structseq[object], tuple[int, str, list[CoroInfo], list[CoroInfo]]):
    """Information about an asyncio task"""
    __match_args__: Final = ("task_id", "task_name", "coroutine_stack", "awaited_by")
    @property
    def task_id(self) -> int:
        """Task ID (memory address)"""
        ...
    @property
    def task_name(self) -> str:
        """Task name"""
        ...
    @property
    def coroutine_stack(self) -> list[CoroInfo]:
        """Coroutine call stack"""
        ...
    @property
    def awaited_by(self) -> list[CoroInfo]:
        """Tasks awaiting this task"""
        ...

@final
class ThreadInfo(structseq[object], tuple[int, int, list[_Frame]]):
    """Information about a thread"""
    __match_args__: Final = ("thread_id", "status", "frame_info")
    @property
    def thread_id(self) -> int:
        """Thread ID"""
        ...
    @property
    def status(self) -> int: ...
    @property
    def frame_info(self) -> list[_Frame]:
        """Frame information"""
        ...

@final
class InterpreterInfo(structseq[object], tuple[int, list[ThreadInfo]]):
    __match_args__: Final = ("interpreter_id", "threads")
    @property
    def interpreter_id(self) -> int: ...
    @property
    def threads(self) -> list[ThreadInfo]: ...

@final
class AwaitedInfo(structseq[object], tuple[int, list[TaskInfo]]):
    """Information about what a thread is awaiting"""
    __match_args__: Final = ("thread_id", "awaited_by")
    @property
    def thread_id(self) -> int:
        """Thread ID"""
        ...
    @property
    def awaited_by(self) -> list[TaskInfo]:
        """List of tasks awaited by this thread"""
        ...

@final
class GCStatsInfo(structseq[object], tuple[int, int, int, int, int, int, int, int, int, float]):
    __match_args__: Final = (
        "gen",
        "iid",
        "ts_start",
        "ts_stop",
        "collections",
        "collected",
        "uncollectable",
        "candidates",
        "heap_size",
        "duration",
    )
    @property
    def gen(self) -> int: ...
    @property
    def iid(self) -> int: ...
    @property
    def ts_start(self) -> int: ...
    @property
    def ts_stop(self) -> int: ...
    @property
    def collections(self) -> int: ...
    @property
    def collected(self) -> int: ...
    @property
    def uncollectable(self) -> int: ...
    @property
    def candidates(self) -> int: ...
    @property
    def heap_size(self) -> int: ...
    @property
    def duration(self) -> float: ...

@final
class RemoteUnwinder:
    """RemoteUnwinder(pid): Inspect stack of a remote Python process."""
    def __init__(
        self,
        pid: int,
        *,
        all_threads: bool = False,
        only_active_thread: bool = False,
        mode: int = 0,
        debug: bool = False,
        skip_non_matching_threads: bool = True,
        native: bool = False,
        gc: bool = False,
        opcodes: bool = False,
        cache_frames: bool = False,
        stats: bool = False,
    ) -> None: ...
    def get_stack_trace(self) -> list[InterpreterInfo]:
        """
        Returns a list of stack traces for threads in the target process.

        Each element in the returned list is a tuple of (thread_id, frame_list), where:
        - thread_id is the OS thread identifier
        - frame_list is a list of tuples (function_name, filename, line_number) representing
          the Python stack frames for that thread, ordered from most recent to oldest

        The threads returned depend on the initialization parameters:
        - If only_active_thread was True: returns only the thread holding the GIL
        - If all_threads was True: returns all threads
        - Otherwise: returns only the main thread

        Example:
            [
                (1234, [
                    ('process_data', 'worker.py', 127),
                    ('run_worker', 'worker.py', 45),
                    ('main', 'app.py', 23)
                ]),
                (1235, [
                    ('handle_request', 'server.py', 89),
                    ('serve_forever', 'server.py', 52)
                ])
            ]

        Raises:
            RuntimeError: If there is an error copying memory from the target process
            OSError: If there is an error accessing the target process
            PermissionError: If access to the target process is denied
            UnicodeDecodeError: If there is an error decoding strings from the target process
        """
        ...
    def get_all_awaited_by(self) -> list[AwaitedInfo]:
        """
        Get all tasks and their awaited_by relationships from the remote process.

        This provides a tree structure showing which tasks are waiting for other tasks.

        For each task, returns:
        1. The call stack frames leading to where the task is currently executing
        2. The name of the task
        3. A list of tasks that this task is waiting for, with their own frames/names/etc

        Returns a list of [frames, task_name, subtasks] where:
        - frames: List of (func_name, filename, lineno) showing the call stack
        - task_name: String identifier for the task
        - subtasks: List of tasks being awaited by this task, in same format

        Raises:
            RuntimeError: If AsyncioDebug section is not available in the remote process
            MemoryError: If memory allocation fails
            OSError: If reading from the remote process fails

        Example output:
        [
            [
                [("c5", "script.py", 10), ("c4", "script.py", 14)],
                "c2_root",
                [
                    [
                        [("c1", "script.py", 23)],
                        "sub_main_2",
                        [...]
                    ],
                    [...]
                ]
            ]
        ]
        """
        ...
    def get_async_stack_trace(self) -> list[AwaitedInfo]:
        """
        Get the currently running async tasks and their dependency graphs from the remote process.

        This returns information about running tasks and all tasks that are waiting for them,
        forming a complete dependency graph for each thread's active task.

        For each thread with a running task, returns the running task plus all tasks that
        transitively depend on it (tasks waiting for the running task, tasks waiting for
        those tasks, etc.).

        Returns a list of per-thread results, where each thread result contains:
        - Thread ID
        - List of task information for the running task and all its waiters

        Each task info contains:
        - Task ID (memory address)
        - Task name
        - Call stack frames: List of (func_name, filename, lineno)
        - List of tasks waiting for this task (recursive structure)

        Raises:
            RuntimeError: If AsyncioDebug section is not available in the target process
            MemoryError: If memory allocation fails
            OSError: If reading from the remote process fails

        Example output (similar structure to get_all_awaited_by but only for running tasks):
        [
            (140234, [
                (4345585712, 'main_task',
                 [("run_server", "server.py", 127), ("main", "app.py", 23)],
                 [
                     (4345585800, 'worker_1', [...], [...]),
                     (4345585900, 'worker_2', [...], [...])
                 ])
            ])
        ]
        """
        ...
    def get_stats(self) -> _Stats: ...
    def pause_threads(self) -> bool: ...
    def resume_threads(self) -> bool: ...

@final
class GCMonitor:
    def __init__(self, pid: int, *, debug: bool = False) -> None: ...
    def get_gc_stats(self, all_interpreters: bool = False) -> list[GCStatsInfo]: ...

@final
class BinaryWriter:
    def __init__(
        self, filename: StrOrBytesPath, sample_interval_us: int, start_time_us: int, *, compression: int = 0
    ) -> None: ...
    @property
    def total_samples(self) -> int: ...
    def write_sample(self, stack_frames: list[InterpreterInfo], timestamp_us: int) -> None: ...
    def finalize(self) -> None: ...
    def close(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: object = None, exc_val: object = None, exc_tb: object = None) -> bool: ...
    def get_stats(self) -> _Stats: ...

@final
class BinaryReader:
    def __init__(self, filename: StrOrBytesPath) -> None: ...
    @property
    def sample_count(self) -> int: ...
    @property
    def sample_interval_us(self) -> int: ...
    def replay(self, collector: object, progress_callback: Callable[[int, int], object] | None = None) -> int: ...
    def get_info(self) -> dict[str, object]: ...
    def get_stats(self) -> _Stats: ...
    def close(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: object = None, exc_val: object = None, exc_tb: object = None) -> bool: ...

def zstd_available() -> bool: ...
def get_child_pids(pid: int, *, recursive: bool = True) -> list[int]: ...
def is_python_process(pid: int) -> bool: ...
def get_gc_stats(pid: int, *, all_interpreters: bool = False) -> list[GCStatsInfo]: ...
