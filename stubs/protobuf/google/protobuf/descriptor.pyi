from collections.abc import Mapping, Sequence
from typing import Any

from .descriptor_pb2 import (
    DescriptorProto,
    EnumDescriptorProto,
    EnumOptions,
    EnumValueOptions,
    FieldOptions,
    FileDescriptorProto,
    FileOptions,
    MessageOptions,
    MethodDescriptorProto,
    MethodOptions,
    OneofOptions,
    ServiceDescriptorProto,
    ServiceOptions,
)
from .descriptor_pool import DescriptorPool
from .message import Message

class Error(Exception):
    """Base error for this module."""
    ...
class TypeTransformationError(Error):
    """Error transforming between python proto type and corresponding C++ type."""
    ...

class DescriptorMetaclass(type):
    def __instancecheck__(cls, obj: object) -> bool: ...

_internal_create_key: object
_USE_C_DESCRIPTORS: bool

class DescriptorBase(metaclass=DescriptorMetaclass):
    has_options: bool
    def __init__(self, file, options, serialized_options, options_class_name) -> None: ...
    def GetOptions(self) -> Any: ...  # Any: overridden with specific *Options in subclasses

class _NestedDescriptorBase(DescriptorBase):
    name: str
    full_name: str
    file: FileDescriptor
    containing_type: Descriptor | None
    def __init__(
        self,
        options,
        options_class_name,
        name,
        full_name,
        file,
        containing_type,
        serialized_start=None,
        serialized_end=None,
        serialized_options=None,
    ) -> None: ...
    def CopyToProto(self, proto: Any) -> None: ...  # Any: overridden with specific *Proto in subclasses

class Descriptor(_NestedDescriptorBase):
    fields: Sequence[FieldDescriptor]
    fields_by_number: Mapping[int, FieldDescriptor]
    fields_by_name: Mapping[str, FieldDescriptor]
    @property
    def fields_by_camelcase_name(self) -> Mapping[str, FieldDescriptor]: ...
    nested_types: Sequence[Descriptor]
    nested_types_by_name: Mapping[str, Descriptor]
    enum_types: Sequence[EnumDescriptor]
    enum_types_by_name: Mapping[str, EnumDescriptor]
    enum_values_by_name: dict[str, EnumValueDescriptor]
    extensions: Sequence[FieldDescriptor]
    extensions_by_name: Mapping[str, FieldDescriptor]
    is_extendable: bool
    extension_ranges: list[tuple[int, int]]
    oneofs: Sequence[OneofDescriptor]
    oneofs_by_name: Mapping[str, OneofDescriptor]
    def __init__(
        self,
        name: str,
        full_name: str,
        filename: str | None,
        containing_type: Descriptor | None,
        fields: list[FieldDescriptor],
        nested_types: list[FieldDescriptor],
        enum_types: list[EnumDescriptor],
        extensions: list[FieldDescriptor],
        options: MessageOptions | None = None,
        serialized_options: bytes | None = None,
        is_extendable: bool | None = True,
        extension_ranges: list[tuple[int, int]] | None = None,
        oneofs: list[OneofDescriptor] | None = None,
        file: FileDescriptor | None = None,
        serialized_start: int | None = None,
        serialized_end: int | None = None,
        syntax: str | None = None,
        is_map_entry: bool = False,
        create_key: object | None = None,
    ): ...
    def EnumValueName(self, enum: str, value: int) -> str: ...
    def CopyToProto(self, proto: DescriptorProto) -> None: ...
    def GetOptions(self) -> MessageOptions: ...

class FieldDescriptor(DescriptorBase):
    TYPE_DOUBLE: int
    TYPE_FLOAT: int
    TYPE_INT64: int
    TYPE_UINT64: int
    TYPE_INT32: int
    TYPE_FIXED64: int
    TYPE_FIXED32: int
    TYPE_BOOL: int
    TYPE_STRING: int
    TYPE_GROUP: int
    TYPE_MESSAGE: int
    TYPE_BYTES: int
    TYPE_UINT32: int
    TYPE_ENUM: int
    TYPE_SFIXED32: int
    TYPE_SFIXED64: int
    TYPE_SINT32: int
    TYPE_SINT64: int
    MAX_TYPE: int
    CPPTYPE_INT32: int
    CPPTYPE_INT64: int
    CPPTYPE_UINT32: int
    CPPTYPE_UINT64: int
    CPPTYPE_DOUBLE: int
    CPPTYPE_FLOAT: int
    CPPTYPE_BOOL: int
    CPPTYPE_ENUM: int
    CPPTYPE_STRING: int
    CPPTYPE_MESSAGE: int
    MAX_CPPTYPE: int
    LABEL_OPTIONAL: int
    LABEL_REQUIRED: int
    LABEL_REPEATED: int
    MAX_LABEL: int
    MAX_FIELD_NUMBER: int
    FIRST_RESERVED_FIELD_NUMBER: int
    LAST_RESERVED_FIELD_NUMBER: int
    def __new__(
        cls,
        name,
        full_name,
        index,
        number,
        type,
        cpp_type,
        label,
        default_value,
        message_type,
        enum_type,
        containing_type,
        is_extension,
        extension_scope,
        options=None,
        serialized_options=None,
        has_default_value=True,
        containing_oneof=None,
        json_name=None,
        file=None,
        create_key=None,
    ): ...
    name: str
    full_name: str
    index: int
    number: int
    type: int
    cpp_type: int
    @property
    def is_required(self) -> bool:
        """Returns if the field is required."""
        ...
    @property
    def is_repeated(self) -> bool:
        """Returns if the field is repeated."""
        ...
    @property
    def camelcase_name(self) -> str:
        """
        Camelcase name of this field.

        Returns:
          str: the name in CamelCase.
        """
        ...
    @property
    def has_presence(self) -> bool:
        """
        Whether the field distinguishes between unpopulated and default values.

        Raises:
          RuntimeError: singular field that is not linked with message nor file.
        """
        ...
    @property
    def is_packed(self) -> bool: ...
    has_default_value: bool
    default_value: Any  # Any: str, int, float, bytes, or bool
    containing_type: Descriptor | None
    message_type: Descriptor | None
    enum_type: EnumDescriptor | None
    is_extension: bool
    extension_scope: Descriptor | None
    containing_oneof: OneofDescriptor | None
    json_name: str
    def __init__(
        self,
        name,
        full_name,
        index,
        number,
        type,
        cpp_type,
        label,
        default_value,
        message_type,
        enum_type,
        containing_type,
        is_extension,
        extension_scope,
        options=None,
        serialized_options=None,
        has_default_value=True,
        containing_oneof=None,
        json_name=None,
        file=None,
        create_key=None,
    ) -> None:
        """
        The arguments are as described in the description of FieldDescriptor

        attributes above.

        Note that containing_type may be None, and may be set later if necessary
        (to deal with circular references between message types, for example).
        Likewise for extension_scope.
        """
        ...
    @staticmethod
    def ProtoTypeToCppProtoType(proto_type: int) -> int: ...
    def GetOptions(self) -> FieldOptions: ...

class EnumDescriptor(_NestedDescriptorBase):
    """
    Descriptor for an enum defined in a .proto file.

    Attributes:
      name (str): Name of the enum type.
      full_name (str): Full name of the type, including package name and any
        enclosing type(s).
      values (list[EnumValueDescriptor]): List of the values in this enum.
      values_by_name (dict(str, EnumValueDescriptor)): Same as :attr:`values`, but
        indexed by the "name" field of each EnumValueDescriptor.
      values_by_number (dict(int, EnumValueDescriptor)): Same as :attr:`values`,
        but indexed by the "number" field of each EnumValueDescriptor.
      containing_type (Descriptor): Descriptor of the immediate containing type of
        this enum, or None if this is an enum defined at the top level in a .proto
        file.  Set by Descriptor's constructor if we're passed into one.
      file (FileDescriptor): Reference to file descriptor.
      options (descriptor_pb2.EnumOptions): Enum options message or None to use
        default enum options.
    """
    def __new__(
        cls,
        name,
        full_name,
        filename,
        values,
        containing_type=None,
        options=None,
        serialized_options=None,
        file=None,
        serialized_start=None,
        serialized_end=None,
        create_key=None,
    ): ...
    values: Sequence[EnumValueDescriptor]
    values_by_name: Mapping[str, EnumValueDescriptor]
    values_by_number: Mapping[int, EnumValueDescriptor]
    def __init__(
        self,
        name,
        full_name,
        filename,
        values,
        containing_type=None,
        options=None,
        serialized_options=None,
        file=None,
        serialized_start=None,
        serialized_end=None,
        create_key=None,
    ) -> None: ...
    @property
    def is_closed(self) -> bool: ...
    def CopyToProto(self, proto: EnumDescriptorProto) -> None: ...
    def GetOptions(self) -> EnumOptions: ...

class EnumValueDescriptor(DescriptorBase):
    """
    Descriptor for a single value within an enum.

    Attributes:
      name (str): Name of this value.
      index (int): Dense, 0-indexed index giving the order that this value appears
        textually within its enum in the .proto file.
      number (int): Actual number assigned to this enum value.
      type (EnumDescriptor): :class:`EnumDescriptor` to which this value belongs.
        Set by :class:`EnumDescriptor`'s constructor if we're passed into one.
      options (descriptor_pb2.EnumValueOptions): Enum value options message or
        None to use default enum value options options.
    """
    def __new__(cls, name, index, number, type=None, options=None, serialized_options=None, create_key=None): ...
    name: str
    index: int
    number: int
    type: EnumDescriptor
    def __init__(self, name, index, number, type=None, options=None, serialized_options=None, create_key=None) -> None: ...
    def GetOptions(self) -> EnumValueOptions: ...

class OneofDescriptor(DescriptorBase):
    def __new__(cls, name, full_name, index, containing_type, fields, options=None, serialized_options=None, create_key=None): ...
    name: str
    full_name: str
    index: int
    containing_type: Descriptor
    fields: Sequence[FieldDescriptor]
    def __init__(
        self, name, full_name, index, containing_type, fields, options=None, serialized_options=None, create_key=None
    ) -> None:
        """Arguments are as described in the attribute description above."""
        ...
    def GetOptions(self) -> OneofOptions:
        """
        Retrieves descriptor options.

        Returns:
          The options set on this descriptor.
        """
        ...

class ServiceDescriptor(_NestedDescriptorBase):
    index: int
    methods: Sequence[MethodDescriptor]
    methods_by_name: Mapping[str, MethodDescriptor]
    def __init__(
        self,
        name: str,
        full_name: str,
        index: int,
        methods: list[MethodDescriptor],
        options: ServiceOptions | None = None,
        serialized_options: bytes | None = None,
        file: FileDescriptor | None = None,
        serialized_start: int | None = None,
        serialized_end: int | None = None,
        create_key: object | None = None,
    ): ...
    def FindMethodByName(self, name: str) -> MethodDescriptor: ...
    def CopyToProto(self, proto: ServiceDescriptorProto) -> None: ...
    def GetOptions(self) -> ServiceOptions: ...

class MethodDescriptor(DescriptorBase):
    """
    Descriptor for a method in a service.

    Attributes:
      name (str): Name of the method within the service.
      full_name (str): Full name of method.
      index (int): 0-indexed index of the method inside the service.
      containing_service (ServiceDescriptor): The service that contains this
        method.
      input_type (Descriptor): The descriptor of the message that this method
        accepts.
      output_type (Descriptor): The descriptor of the message that this method
        returns.
      client_streaming (bool): Whether this method uses client streaming.
      server_streaming (bool): Whether this method uses server streaming.
      options (descriptor_pb2.MethodOptions or None): Method options message, or
        None to use default method options.
    """
    def __new__(
        cls,
        name,
        full_name,
        index,
        containing_service,
        input_type,
        output_type,
        client_streaming=False,
        server_streaming=False,
        options=None,
        serialized_options=None,
        create_key=None,
    ): ...
    name: str
    full_name: str
    index: int
    containing_service: ServiceDescriptor
    input_type: Descriptor
    output_type: Descriptor
    client_streaming: bool
    server_streaming: bool
    def __init__(
        self,
        name,
        full_name,
        index,
        containing_service,
        input_type,
        output_type,
        client_streaming=False,
        server_streaming=False,
        options=None,
        serialized_options=None,
        create_key=None,
    ) -> None: ...
    def CopyToProto(self, proto: MethodDescriptorProto) -> None: ...
    def GetOptions(self) -> MethodOptions: ...

class FileDescriptor(DescriptorBase):
    """
    Descriptor for a file. Mimics the descriptor_pb2.FileDescriptorProto.

    Note that :attr:`enum_types_by_name`, :attr:`extensions_by_name`, and
    :attr:`dependencies` fields are only set by the
    :py:mod:`google.protobuf.message_factory` module, and not by the generated
    proto code.

    Attributes:
      name (str): Name of file, relative to root of source tree.
      package (str): Name of the package
      edition (Edition): Enum value indicating edition of the file
      serialized_pb (bytes): Byte string of serialized
        :class:`descriptor_pb2.FileDescriptorProto`.
      dependencies (list[FileDescriptor]): List of other :class:`FileDescriptor`
        objects this :class:`FileDescriptor` depends on.
      public_dependencies (list[FileDescriptor]): A subset of
        :attr:`dependencies`, which were declared as "public".
      message_types_by_name (dict(str, Descriptor)): Mapping from message names to
        their :class:`Descriptor`.
      enum_types_by_name (dict(str, EnumDescriptor)): Mapping from enum names to
        their :class:`EnumDescriptor`.
      extensions_by_name (dict(str, FieldDescriptor)): Mapping from extension
        names declared at file scope to their :class:`FieldDescriptor`.
      services_by_name (dict(str, ServiceDescriptor)): Mapping from services'
        names to their :class:`ServiceDescriptor`.
      pool (DescriptorPool): The pool this descriptor belongs to.  When not passed
        to the constructor, the global default pool is used.
    """
    def __new__(
        cls,
        name,
        package,
        options=None,
        serialized_options=None,
        serialized_pb=None,
        dependencies=None,
        public_dependencies=None,
        syntax=None,
        edition=None,
        pool=None,
        create_key=None,
    ): ...
    _options: Any
    pool: DescriptorPool
    message_types_by_name: Mapping[str, Descriptor]
    name: str
    package: str
    serialized_pb: bytes
    enum_types_by_name: Mapping[str, EnumDescriptor]
    extensions_by_name: Mapping[str, FieldDescriptor]
    services_by_name: Mapping[str, ServiceDescriptor]
    dependencies: Sequence[FileDescriptor]
    public_dependencies: Sequence[FileDescriptor]
    def __init__(
        self,
        name,
        package,
        options=None,
        serialized_options=None,
        serialized_pb=None,
        dependencies=None,
        public_dependencies=None,
        syntax=None,
        edition=None,
        pool=None,
        create_key=None,
    ) -> None: ...
    def CopyToProto(self, proto: FileDescriptorProto) -> None: ...
    def GetOptions(self) -> FileOptions: ...

def _ParseOptions(message: Message, string: bytes) -> Message: ...
def MakeDescriptor(
    desc_proto: DescriptorProto,
    package: str = "",
    build_file_if_cpp: bool = True,
    syntax: str | None = None,
    edition: str | None = None,
    file_desc: FileDescriptor | None = None,
) -> Descriptor: ...
