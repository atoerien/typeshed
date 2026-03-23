"""
General utility functions common to client and server.

This module contains a collection of general purpose utility functions.
"""

def IIDToInterfaceName(iid) -> str:
    """
    Converts an IID to a string interface name.

    Used primarily for debugging purposes, this allows a cryptic IID to
    be converted to a useful string name.  This will firstly look for interfaces
    known (ie, registered) by pythoncom.  If not known, it will look in the
    registry for a registered interface.

    iid -- An IID object.

    Result -- Always a string - either an interface name, or '<Unregistered interface>'
    """
    ...
