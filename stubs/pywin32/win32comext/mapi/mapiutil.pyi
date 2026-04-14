prTable: dict[int, str]

def GetPropTagName(pt): ...

mapiErrorTable: dict[int, str]

def GetScodeString(hr): ...

ptTable: dict[int, str]

def GetMapiTypeName(propType, rawType: bool = ...):
    """Given a mapi type flag, return a string description of the type"""
    ...
def GetProperties(obj, propList):
    """
    Given a MAPI object and a list of properties, return a list of property values.

    Allows a single property to be passed, and the result is a single object.

    Each request property can be an integer or a string.  Of a string, it is
    automatically converted to an integer via the GetIdsFromNames function.

    If the property fetch fails, the result is None.
    """
    ...
def GetAllProperties(obj, make_tag_names: bool = ...): ...
def SetPropertyValue(obj, prop, val) -> None: ...
def SetProperties(msg, propDict) -> None:
    """
    Given a Python dictionary, set the objects properties.

    If the dictionary key is a string, then a property ID is queried
    otherwise the ID is assumed native.

    Coded for maximum efficiency wrt server calls - ie, maximum of
    2 calls made to the object, regardless of the dictionary contents
    (only 1 if dictionary full of int keys)
    """
    ...
