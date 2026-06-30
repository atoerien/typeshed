"""
This module manages the version specific aspects of bytecode instrumentation.

Accross Python versions there are variations in:
    - Instructions
    - Instruction arguments
    - Shape of a code object
    - Construction of the lnotab

Currently supported python versions are:
    - 3.11
    - 3.12
    - 3.13
    - 3.14
"""

import types
from typing import Final

PYTHON_VERSION: Final[tuple[int, int]]
CONDITIONAL_JUMPS: Final[list[str]]
UNCONDITIONAL_JUMPS: Final[list[str]]
ENDS_FUNCTION: Final[list[str]]
HAVE_REL_REFERENCE: Final[list[str]]
HAVE_ABS_REFERENCE: Final[list[str]]
REL_REFERENCE_IS_INVERTED: Final[list[str]]

def rel_reference_scale(opname: str) -> int: ...

REVERSE_CMP_OP: Final[list[int]]

def jump_arg_bytes(arg: int) -> int: ...
def add_bytes_to_jump_arg(arg: int, size: int) -> int: ...

class ExceptionTableEntry:
    def __init__(self, start_offset: int, end_offset: int, target: int, depth: int, lasti: bool) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class ExceptionTable:
    def __init__(self, entries: list[ExceptionTableEntry]) -> None: ...
    def __eq__(self, other: object) -> bool: ...

def generate_exceptiontable(original_code: types.CodeType, exception_table_entries: list[ExceptionTableEntry]) -> bytes: ...

CONST_PUSH_INSTRS: Final[set[str]]

def is_func_start_resume(opname: str, arg: int | None) -> bool:
    """
    Returns True if this is the function-entry RESUME instruction.

    From 3.13 onward RESUME's oparg may have RESUME_OPARG_DEPTH1_MASK (0x4)
    set when the resume point is one try-block deep, so only the low two bits
    encode the resume kind (RESUME_AT_FUNC_START == 0).
    """
    ...
def has_argument(op: int) -> bool:
    """
    Returns whether `op` takes an argument.

    HAVE_ARGUMENT is no longer a reliable boundary in 3.12+ (and is formally
    meaningless in 3.14, where e.g. TO_BOOL < HAVE_ARGUMENT yet RESUME >
    HAVE_ARGUMENT). dis.hasarg is the authoritative source.
    """
    ...
