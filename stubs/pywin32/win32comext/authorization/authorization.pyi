"""Module containing support for authorization COM interfaces."""

import _win32typing

def EditSecurity(hwndOwner, psi):
    """Creates a security descriptor editor dialog"""
    ...

IID_ISecurityInformation: _win32typing.PyIID
