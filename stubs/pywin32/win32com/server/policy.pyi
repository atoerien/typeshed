"""
Policies

Note that Dispatchers are now implemented in "dispatcher.py", but
are still documented here.

Policies

 A policy is an object which manages the interaction between a public
 Python object, and COM .  In simple terms, the policy object is the
 object which is actually called by COM, and it invokes the requested
 method, fetches/sets the requested property, etc.  See the
 @win32com.server.policy.CreateInstance@ method for a description of
 how a policy is specified or created.

 Exactly how a policy determines which underlying object method/property
 is obtained is up to the policy.  A few policies are provided, but you
 can build your own.  See each policy class for a description of how it
 implements its policy.

 There is a policy that allows the object to specify exactly which
 methods and properties will be exposed.  There is also a policy that
 will dynamically expose all Python methods and properties - even those
 added after the object has been instantiated.

Dispatchers

 A Dispatcher is a level in front of a Policy.  A dispatcher is the
 thing which actually receives the COM calls, and passes them to the
 policy object (which in turn somehow does something with the wrapped
 object).

 It is important to note that a policy does not need to have a dispatcher.
 A dispatcher has the same interface as a policy, and simply steps in its
 place, delegating to the real policy.  The primary use for a Dispatcher
 is to support debugging when necessary, but without imposing overheads
 when not (ie, by not using a dispatcher at all).

 There are a few dispatchers provided - "tracing" dispatchers which simply
 prints calls and args (including a variation which uses
 win32api.OutputDebugString), and a "debugger" dispatcher, which can
 invoke the debugger when necessary.

Error Handling

 It is important to realise that the caller of these interfaces may
 not be Python.  Therefore, general Python exceptions and tracebacks aren't
 much use.

 In general, there is an COMException class that should be raised, to allow
 the framework to extract rich COM type error information.

 The general rule is that the **only** exception returned from Python COM
 Server code should be an COMException instance.  Any other Python exception
 should be considered an implementation bug in the server (if not, it
 should be handled, and an appropriate COMException instance raised).  Any
 other exception is considered "unexpected", and a dispatcher may take
 special action (see Dispatchers above)

 Occasionally, the implementation will raise the policy.error error.
 This usually means there is a problem in the implementation that the
 Python programmer should fix.

 For example, if policy is asked to wrap an object which it can not
 support (because, eg, it does not provide _public_methods_ or _dynamic_)
 then policy.error will be raised, indicating it is a Python programmers
 problem, rather than a COM error.
"""

from _typeshed import Incomplete
from abc import ABC, abstractmethod
from typing import Any, Final

import _win32typing

__author__: Final[str]
S_OK: Final = 0
IDispatchType: Incomplete
IUnknownType: Incomplete
regSpec: str
regPolicy: str
regDispatcher: str
regAddnPath: str

def CreateInstance(clsid, reqIID: _win32typing.PyIID) -> _win32typing.PyIUnknown:
    """
    Create a new instance of the specified IID

    The COM framework **always** calls this function to create a new
    instance for the specified CLSID.  This function looks up the
    registry for the name of a policy, creates the policy, and asks the
    policy to create the specified object by calling the _CreateInstance_ method.

    Exactly how the policy creates the instance is up to the policy.  See the
    specific policy documentation for more details.
    """
    ...

class BasicWrapPolicy(ABC):
    """
    The base class of policies.

    Normally not used directly (use a child class, instead)

    This policy assumes we are wrapping another object
    as the COM server.  This supports the delegation of the core COM entry points
    to either the wrapped object, or to a child class.

    This policy supports the following special attributes on the wrapped object

    _query_interface_ -- A handler which can respond to the COM 'QueryInterface' call.
    _com_interfaces_ -- An optional list of IIDs which the interface will assume are
        valid for the object.
    _invoke_ -- A handler which can respond to the COM 'Invoke' call.  If this attribute
        is not provided, then the default policy implementation is used.  If this attribute
        does exist, it is responsible for providing all required functionality - ie, the
        policy _invoke_ method is not invoked at all (and nor are you able to call it!)
    _getidsofnames_ -- A handler which can respond to the COM 'GetIDsOfNames' call.  If this attribute
        is not provided, then the default policy implementation is used.  If this attribute
        does exist, it is responsible for providing all required functionality - ie, the
        policy _getidsofnames_ method is not invoked at all (and nor are you able to call it!)

    IDispatchEx functionality:

    _invokeex_ -- Very similar to _invoke_, except slightly different arguments are used.
        And the result is just the _real_ result (rather than the (hresult, argErr, realResult)
        tuple that _invoke_ uses.
        This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)
    _getdispid_ -- Very similar to _getidsofnames_, except slightly different arguments are used,
        and only 1 property at a time can be fetched (which is all we support in getidsofnames anyway!)
        This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)
    _getnextdispid_- uses self._name_to_dispid_ to enumerate the DISPIDs
    """
    def __init__(self, object) -> None:
        """
        Initialise the policy object

        Params:

        object -- The object to wrap.  May be None *iff* @BasicWrapPolicy._CreateInstance_@ will be
        called immediately after this to setup a brand new object
        """
        ...
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider) -> tuple[Incomplete]:
        """
        The main COM entry-point for InvokeEx.

        This calls the _invokeex_ helper.
        """
        ...
    @abstractmethod
    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider) -> tuple[Incomplete]:
        """
        A stub for _invokeex_ - should never be called.

        Simply raises an exception.
        """
        ...

class MappedWrapPolicy(BasicWrapPolicy):
    """
    Wraps an object using maps to do its magic

    This policy wraps up a Python object, using a number of maps
    which translate from a Dispatch ID and flags, into an object to call/getattr, etc.

    It is the responsibility of derived classes to determine exactly how the
    maps are filled (ie, the derived classes determine the map filling policy.

    This policy supports the following special attributes on the wrapped object

    _dispid_to_func_/_dispid_to_get_/_dispid_to_put_ -- These are dictionaries
      (keyed by integer dispid, values are string attribute names) which the COM
      implementation uses when it is processing COM requests.  Note that the implementation
      uses this dictionary for its own purposes - not a copy - which means the contents of
      these dictionaries will change as the object is used.
    """
    _dispid_to_func_: dict[int, str]
    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider) -> tuple[Incomplete]:
        """
        A stub for _invokeex_ - should never be called.

        Simply raises an exception.
        """
        ...

class DesignatedWrapPolicy(MappedWrapPolicy):
    """
    A policy which uses a mapping to link functions and dispid

     A MappedWrappedPolicy which allows the wrapped object to specify, via certain
     special named attributes, exactly which methods and properties are exposed.

     All a wrapped object need do is provide the special attributes, and the policy
     will handle everything else.

     Attributes:

     _public_methods_ -- Required, unless a typelib GUID is given -- A list
                  of strings, which must be the names of methods the object
                  provides.  These methods will be exposed and callable
                  from other COM hosts.
     _public_attrs_ A list of strings, which must be the names of attributes on the object.
                  These attributes will be exposed and readable and possibly writeable from other COM hosts.
     _readonly_attrs_ -- A list of strings, which must also appear in _public_attrs.  These
                  attributes will be readable, but not writable, by other COM hosts.
     _value_ -- A method that will be called if the COM host requests the "default" method
                  (ie, calls Invoke with dispid==DISPID_VALUE)
     _NewEnum -- A method that will be called if the COM host requests an enumerator on the
                  object (ie, calls Invoke with dispid==DISPID_NEWENUM.)
                  It is the responsibility of the method to ensure the returned
                  object conforms to the required Enum interface.

    _typelib_guid_ -- The GUID of the typelibrary with interface definitions we use.
    _typelib_version_ -- A tuple of (major, minor) with a default of 1,1
    _typelib_lcid_ -- The LCID of the typelib, default = LOCALE_USER_DEFAULT

     _Evaluate -- Dunno what this means, except the host has called Invoke with dispid==DISPID_EVALUATE!
                  See the COM documentation for details.
    """
    ...
class EventHandlerPolicy(DesignatedWrapPolicy):
    """
    The default policy used by event handlers in the win32com.client package.

    In addition to the base policy, this provides argument conversion semantics for
    params: dispatch params are converted to dispatch objects

    NOTE: Later, we may allow the object to override this process??
    """
    ...

class DynamicPolicy(BasicWrapPolicy):
    """
    A policy which dynamically (ie, at run-time) determines public interfaces.

    A dynamic policy is used to dynamically dispatch methods and properties to the
    wrapped object.  The list of objects and properties does not need to be known in
    advance, and methods or properties added to the wrapped object after construction
    are also handled.

    The wrapped object must provide the following attributes:

    _dynamic_ -- A method that will be called whenever an invoke on the object
           is called.  The method is called with the name of the underlying method/property
           (ie, the mapping of dispid to/from name has been resolved.)  This name property
           may also be '_value_' to indicate the default, and '_NewEnum' to indicate a new
           enumerator is requested.
    """
    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider) -> tuple[Incomplete]: ...

DefaultPolicy = DesignatedWrapPolicy

# Imports an arbitrary object by it's fully-qualified name.
def resolve_func(spec: str) -> Any:
    """
    Resolve a function by name

    Given a function specified by 'module.function', return a callable object
    (ie, the function itself)
    """
    ...

# Imports and calls an arbitrary callable by it's fully-qualified name.
def call_func(spec: str, *args: Any) -> Any:
    """
    Call a function specified by name.

    Call a function specified by 'module.function' and return the result.
    """
    ...

DISPATCH_METHOD: int
DISPATCH_PROPERTYGET: int
DISPATCH_PROPERTYPUT: int
DISPATCH_PROPERTYPUTREF: int
DISPID_EVALUATE: int
DISPID_NEWENUM: int
DISPID_PROPERTYPUT: int
DISPID_STARTENUM: int
DISPID_VALUE: int
