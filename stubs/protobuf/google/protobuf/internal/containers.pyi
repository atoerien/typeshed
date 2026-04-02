"""
Contains container classes to represent different protocol buffer types.

This file defines container classes which represent categories of protocol
buffer field types which need extra maintenance. Currently these categories
are:

-   Repeated scalar fields - These are all repeated fields which aren't
    composite (e.g. they are of simple types like int32, string, etc).
-   Repeated composite fields - Repeated fields which are composite. This
    includes groups and nested messages.
"""

from collections.abc import Callable, Iterable, Iterator, MutableMapping, MutableSequence, Sequence
from typing import Any, Protocol, SupportsIndex, TypeVar, overload, type_check_only

from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.internal.message_listener import MessageListener
from google.protobuf.internal.python_message import GeneratedProtocolMessageType
from google.protobuf.message import Message

_T = TypeVar("_T")
_K = TypeVar("_K", bound=bool | int | str)
_ScalarV = TypeVar("_ScalarV", bound=bool | int | float | str | bytes)
_MessageV = TypeVar("_MessageV", bound=Message)

@type_check_only
class _ValueChecker(Protocol[_T]):
    def CheckValue(self, proposed_value: _T) -> _T: ...
    def DefaultValue(self) -> _T: ...

class BaseContainer(Sequence[_T]):
    """Base container class."""
    __slots__ = ["_message_listener", "_values"]
    def __init__(self, message_listener: MessageListener) -> None:
        """
        Args:
          message_listener: A MessageListener implementation.
            The RepeatedScalarFieldContainer will call this object's
            Modified() method when it is modified.
        """
        ...
    @overload
    def __getitem__(self, key: SupportsIndex) -> _T:
        """Retrieves item by the specified key."""
        ...
    @overload
    def __getitem__(self, key: slice) -> list[_T]:
        """Retrieves item by the specified key."""
        ...
    def __len__(self) -> int:
        """Returns the number of elements in the container."""
        ...
    def __ne__(self, other: object) -> bool:
        """Checks if another instance isn't equal to this one."""
        ...
    def __hash__(self) -> int: ...
    # Same as list.sort, the extra sort_function kwarg errors in Python 3
    def sort(self, *, key: Callable[[_T], Any] | None = None, reverse: bool = False) -> None: ...
    def reverse(self) -> None: ...

class RepeatedScalarFieldContainer(BaseContainer[_ScalarV], MutableSequence[_ScalarV]):
    """Simple, type-checked, list-like container for holding repeated scalars."""
    __slots__ = ["_type_checker"]
    def __init__(
        self, message_listener: MessageListener, type_checker: _ValueChecker[_ScalarV], field: FieldDescriptor | None = None
    ) -> None:
        """
        Args:

        message_listener: A MessageListener implementation. The
        RepeatedScalarFieldContainer will call this object's Modified() method
        when it is modified.
        type_checker: A type_checkers.ValueChecker instance to run on elements
        inserted into this container.
        """
        ...
    def append(self, value: _ScalarV) -> None:
        """Appends an item to the list. Similar to list.append()."""
        ...
    def insert(self, key: int, value: _ScalarV) -> None:
        """Inserts the item at the specified position. Similar to list.insert()."""
        ...
    def extend(self, elem_seq: Iterable[_ScalarV] | None) -> None:
        """Extends by appending the given iterable. Similar to list.extend()."""
        ...
    def MergeFrom(self, other: RepeatedScalarFieldContainer[_ScalarV] | Iterable[_ScalarV]) -> None:
        """
        Appends the contents of another repeated field of the same type to this
        one. We do not check the types of the individual fields.
        """
        ...
    def remove(self, elem: _ScalarV) -> None:
        """Removes an item from the list. Similar to list.remove()."""
        ...
    def pop(self, key: int = -1) -> _ScalarV:
        """Removes and returns an item at a given index. Similar to list.pop()."""
        ...
    @overload
    def __setitem__(self, key: int, value: _ScalarV) -> None:
        """Sets the item on the specified position."""
        ...
    @overload
    def __setitem__(self, key: slice, value: Iterable[_ScalarV]) -> None:
        """Sets the item on the specified position."""
        ...
    def __delitem__(self, key: int | slice) -> None:
        """Deletes the item at the specified position."""
        ...
    def __eq__(self, other: object) -> bool:
        """Compares the current instance with another one."""
        ...
    def __deepcopy__(self, unused_memo: Any = None) -> RepeatedScalarFieldContainer[_ScalarV]: ...
    def __array__(self, dtype: Any = None, copy: bool | None = None) -> Any: ...  # Any: numpy types

class RepeatedCompositeFieldContainer(BaseContainer[_MessageV], MutableSequence[_MessageV]):
    """Simple, list-like container for holding repeated composite fields."""
    __slots__ = ["_message_descriptor"]
    def __init__(self, message_listener: MessageListener, message_descriptor: Descriptor) -> None:
        """
        Note that we pass in a descriptor instead of the generated directly,
        since at the time we construct a _RepeatedCompositeFieldContainer we
        haven't yet necessarily initialized the type that will be contained in the
        container.

        Args:
          message_listener: A MessageListener implementation.
            The RepeatedCompositeFieldContainer will call this object's
            Modified() method when it is modified.
          message_descriptor: A Descriptor instance describing the protocol type
            that should be present in this container.  We'll use the
            _concrete_class field of this descriptor when the client calls add().
        """
        ...
    def add(self, **kwargs: Any) -> _MessageV:
        """
        Adds a new element at the end of the list and returns it. Keyword
        arguments may be used to initialize the element.
        """
        ...
    def append(self, value: _MessageV) -> None:
        """Appends one element by copying the message."""
        ...
    def insert(self, key: int, value: _MessageV) -> None:
        """Inserts the item at the specified position by copying."""
        ...
    def extend(self, elem_seq: Iterable[_MessageV]) -> None:
        """
        Extends by appending the given sequence of elements of the same type

        as this one, copying each individual message.
        """
        ...
    def MergeFrom(self, other: RepeatedCompositeFieldContainer[_MessageV] | Iterable[_MessageV]) -> None:
        """
        Appends the contents of another repeated field of the same type to this
        one, copying each individual message.
        """
        ...
    def remove(self, elem: _MessageV) -> None:
        """Removes an item from the list. Similar to list.remove()."""
        ...
    def pop(self, key: int = -1) -> _MessageV:
        """Removes and returns an item at a given index. Similar to list.pop()."""
        ...
    @overload
    def __setitem__(self, key: int, value: _MessageV) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: Iterable[_MessageV]) -> None: ...
    def __delitem__(self, key: int | slice) -> None:
        """Deletes the item at the specified position."""
        ...
    def __eq__(self, other: object) -> bool:
        """Compares the current instance with another one."""
        ...

class ScalarMap(MutableMapping[_K, _ScalarV]):
    """Simple, type-checked, dict-like container for holding repeated scalars."""
    __slots__ = ["_key_checker", "_value_checker", "_values", "_message_listener", "_entry_descriptor"]
    def __init__(
        self,
        message_listener: MessageListener,
        key_checker: _ValueChecker[_K],
        value_checker: _ValueChecker[_ScalarV],
        entry_descriptor: Descriptor,
    ) -> None:
        """
        Args:
          message_listener: A MessageListener implementation.
            The ScalarMap will call this object's Modified() method when it
            is modified.
          key_checker: A type_checkers.ValueChecker instance to run on keys
            inserted into this container.
          value_checker: A type_checkers.ValueChecker instance to run on values
            inserted into this container.
          entry_descriptor: The MessageDescriptor of a map entry: key and value.
        """
        ...
    def __getitem__(self, key: _K) -> _ScalarV: ...
    @overload
    def get(self, key: _K, default: None = None) -> _ScalarV | None: ...
    @overload
    def get(self, key: _K, default: _ScalarV) -> _ScalarV: ...
    @overload
    def get(self, key: _K, default: _T) -> _ScalarV | _T: ...
    def __setitem__(self, key: _K, value: _ScalarV) -> None: ...
    def __delitem__(self, key: _K) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_K]: ...
    def __eq__(self, other: object) -> bool: ...
    def setdefault(self, key: _K, value: _ScalarV | None = None) -> _ScalarV: ...
    def MergeFrom(self, other: ScalarMap[_K, _ScalarV]) -> None: ...
    def InvalidateIterators(self) -> None: ...
    def clear(self) -> None: ...
    def GetEntryClass(self) -> GeneratedProtocolMessageType: ...

class MessageMap(MutableMapping[_K, _MessageV]):
    """Simple, type-checked, dict-like container for with submessage values."""
    __slots__ = ["_key_checker", "_values", "_message_listener", "_message_descriptor", "_entry_descriptor"]
    def __init__(
        self,
        message_listener: MessageListener,
        message_descriptor: Descriptor,
        key_checker: _ValueChecker[_K],
        entry_descriptor: Descriptor,
    ) -> None:
        """
        Args:
          message_listener: A MessageListener implementation.
            The ScalarMap will call this object's Modified() method when it
            is modified.
          key_checker: A type_checkers.ValueChecker instance to run on keys
            inserted into this container.
          value_checker: A type_checkers.ValueChecker instance to run on values
            inserted into this container.
          entry_descriptor: The MessageDescriptor of a map entry: key and value.
        """
        ...
    def __getitem__(self, key: _K) -> _MessageV: ...
    def get_or_create(self, key: _K) -> _MessageV:
        """
        get_or_create() is an alias for getitem (ie. map[key]).

        Args:
          key: The key to get or create in the map.

        This is useful in cases where you want to be explicit that the call is
        mutating the map.  This can avoid lint errors for statements like this
        that otherwise would appear to be pointless statements:

          msg.my_map[key]
        """
        ...
    @overload
    def get(self, key: _K, default: None = None) -> _MessageV | None: ...
    @overload
    def get(self, key: _K, default: _MessageV) -> _MessageV: ...
    @overload
    def get(self, key: _K, default: _T) -> _MessageV | _T: ...
    def __setitem__(self, key: _K, value: _MessageV) -> None: ...
    def __delitem__(self, key: _K) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_K]: ...
    def __eq__(self, other: object) -> bool: ...
    def setdefault(self, key: _K, value: _MessageV | None = None) -> _MessageV: ...
    def MergeFrom(self, other: MessageMap[_K, _MessageV]) -> None: ...
    def InvalidateIterators(self) -> None: ...
    def clear(self) -> None: ...
    def GetEntryClass(self) -> GeneratedProtocolMessageType: ...

class UnknownFieldRef:
    def __init__(self, parent: UnknownFieldSet, index: int) -> None: ...
    @property
    def field_number(self) -> int: ...
    @property
    def wire_type(self) -> int: ...
    @property
    def data(self) -> Any: ...  # Any: int, bytes, or UnknownFieldSet

class UnknownFieldSet:
    """UnknownField container"""
    __slots__ = ["_values"]
    def __init__(self) -> None: ...
    def __getitem__(self, index: int) -> UnknownFieldRef: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[UnknownFieldRef]: ...
