"""Compiled extension module that provides access to the memory mapped file API"""

import _win32typing
from win32.lib.pywintypes import error as error

def mmapfile(
    File, Name, MaximumSize: int = ..., FileOffset: int = ..., NumberOfBytesToMap: int = ...
) -> _win32typing.Pymmapfile:
    """Pymmapfile=mmapfile(File,Name,MaximumSize=0,FileOffset=0,NumberOfBytesToMap=0)  Creates a memory mapped file view"""
    ...
