"""Interface to the Windows Console functions for dealing with character-mode applications."""

from typing import Literal, NoReturn, overload

import _win32typing
from win32.lib.pywintypes import error as error

def GetConsoleProcessList() -> tuple[int, ...]:
    """Returns pids of all processes attached to current console"""
    ...
def CreateConsoleScreenBuffer(
    DesiredAccess=..., ShareMode=..., SecurityAttributes: _win32typing.PySECURITY_ATTRIBUTES | None = ..., Flags=...
) -> _win32typing.PyConsoleScreenBuffer:
    """Creates a new console screen buffer"""
    ...
def GetConsoleDisplayMode():
    """Returns the current console's display mode"""
    ...
def AttachConsole(ProcessId) -> None:
    """Attaches calling process to console of another process"""
    ...
def AllocConsole() -> None:
    """Creates a new console for the calling process"""
    ...
def FreeConsole() -> None:
    """Detaches process from its console"""
    ...
def GetConsoleCP():
    """Returns the input code page for calling process's console"""
    ...
def GetConsoleOutputCP():
    """Returns the output code page for calling process's console"""
    ...
def SetConsoleCP(CodePageId) -> None:
    """Sets the input code page for calling process's console"""
    ...
def SetConsoleOutputCP(CodePageID) -> None:
    """Sets the output code page for calling process's console"""
    ...
def GetConsoleSelectionInfo():
    """Returns info on text selection within the current console"""
    ...
def AddConsoleAlias(Source, Target, ExeName) -> None:
    """Creates a new console alias"""
    ...
def GetConsoleAliases(ExeName: str) -> str:
    """Retrieves aliases defined under specified executable"""
    ...
def GetConsoleAliasExes():
    """Lists all executables that have console aliases defined"""
    ...
def GetConsoleWindow():
    """Returns a handle to the console's window, or 0 if none exists"""
    ...
def GetNumberOfConsoleFonts():
    """Returns the number of fonts available to the console"""
    ...
def SetConsoleTitle(ConsoleTitle: str) -> None:
    """Sets the title of calling process's console"""
    ...
def GetConsoleTitle():
    """Returns the title of console to which calling process is attached"""
    ...
@overload
def GenerateConsoleCtrlEvent(CtrlEvent: Literal[1], ProcessGroupId: Literal[0] = 0) -> NoReturn:
    """Sends a control signal to a group of processes attached to a common console"""
    ...
@overload
def GenerateConsoleCtrlEvent(CtrlEvent: Literal[0, 1], ProcessGroupId: int) -> None:
    """Sends a control signal to a group of processes attached to a common console"""
    ...
def GetStdHandle(StdHandle: int) -> _win32typing.PyConsoleScreenBuffer:
    """Returns one of calling process's standard handles"""
    ...

ATTACH_PARENT_PROCESS: int
BACKGROUND_BLUE: int
BACKGROUND_GREEN: int
BACKGROUND_INTENSITY: int
BACKGROUND_RED: int
COMMON_LVB_GRID_HORIZONTAL: int
COMMON_LVB_GRID_LVERTICAL: int
COMMON_LVB_GRID_RVERTICAL: int
COMMON_LVB_LEADING_BYTE: int
COMMON_LVB_REVERSE_VIDEO: int
COMMON_LVB_TRAILING_BYTE: int
COMMON_LVB_UNDERSCORE: int
CONSOLE_FULLSCREEN: int
CONSOLE_FULLSCREEN_HARDWARE: int
CONSOLE_FULLSCREEN_MODE: int
CONSOLE_MOUSE_DOWN: int
CONSOLE_MOUSE_SELECTION: int
CONSOLE_NO_SELECTION: int
CONSOLE_SELECTION_IN_PROGRESS: int
CONSOLE_SELECTION_NOT_EMPTY: int
CONSOLE_TEXTMODE_BUFFER: int
CONSOLE_WINDOWED_MODE: int
CTRL_BREAK_EVENT: int
CTRL_C_EVENT: int
ENABLE_ECHO_INPUT: int
ENABLE_LINE_INPUT: int
ENABLE_MOUSE_INPUT: int
ENABLE_PROCESSED_INPUT: int
ENABLE_PROCESSED_OUTPUT: int
ENABLE_WINDOW_INPUT: int
ENABLE_WRAP_AT_EOL_OUTPUT: int
FOCUS_EVENT: int
FOREGROUND_BLUE: int
FOREGROUND_GREEN: int
FOREGROUND_INTENSITY: int
FOREGROUND_RED: int
KEY_EVENT: int
LOCALE_USER_DEFAULT: int
MENU_EVENT: int
MOUSE_EVENT: int
PyCOORDType = _win32typing.PyCOORD
PyConsoleScreenBufferType = _win32typing.PyConsoleScreenBuffer
PyINPUT_RECORDType = _win32typing.PyINPUT_RECORD
PySMALL_RECTType = _win32typing.PySMALL_RECT
STD_ERROR_HANDLE: int
STD_INPUT_HANDLE: int
STD_OUTPUT_HANDLE: int
WINDOW_BUFFER_SIZE_EVENT: int
