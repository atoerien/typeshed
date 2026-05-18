"""
Simple IOC container.

Classes:

    Container
    MissingDependencyError
    InvalidRegistrationError
    InvalidForwardReferenceError
    MissingDependencyException
    InvalidRegistrationException
    InvalidForwardReferenceException
    Scope

Misc Variables:

    empty
"""

from collections.abc import Callable
from enum import Enum
from typing import Any, Final, Generic, NamedTuple, NewType, TypeVar, overload

__version__: str

class MissingDependencyException(Exception):
    """Deprecated alias for MissingDependencyError."""
    ...
class MissingDependencyError(MissingDependencyException):
    """
    Raised when a service, or one of its dependencies, is not registered.

    Examples:
        >>> import punq
        >>> container = punq.Container()
        >>> container.resolve("foo")
        Traceback (most recent call last):
        punq.MissingDependencyError: Failed to resolve implementation for foo
    """
    ...
class InvalidRegistrationException(Exception):
    """Deprecated alias for InvalidRegistrationError."""
    ...
class InvalidRegistrationError(InvalidRegistrationException):
    """Raised when a registration would result in an unresolvable service."""
    ...
class InvalidForwardReferenceException(Exception):
    """Deprecated alias for InvalidForwardReferenceError."""
    ...
class InvalidForwardReferenceError(InvalidForwardReferenceException):
    """
    Raised when a registered service has a forward reference that can't be resolved.

    Examples:
        In this example, we register a service with a string as a type annotation.
        When we try to inspect the constructor for the service we fail with an
        InvalidForwardReferenceError

        >>> from dataclasses import dataclass
        >>> from punq import Container
        >>> @dataclass
        ... class Client:
        ...     dep: 'Dependency'
        >>> container = Container()
        >>> container.register(Client)
        Traceback (most recent call last):
        ...
        punq.InvalidForwardReferenceError: name 'Dependency' is not defined


        This error can be resolved by first registering a type with the name
        'Dependency' in the container.

        >>> class Dependency:
        ...     pass
        ...
        >>> container.register(Dependency)
        <punq.Container object at 0x...>
        >>> container.register(Client)
        <punq.Container object at 0x...>
        >>> container.resolve(Client)
        Client(dep=<punq.Dependency object at 0x...>)


        Alternatively, we can register a type using the literal key 'Dependency'.

        >>> class AlternativeDependency:
        ...     pass
        ...
        >>> container = Container()
        >>> container.register('Dependency', AlternativeDependency)
        <punq.Container object at 0x...>
        >>> container.register(Client)
        <punq.Container object at 0x...>
        >>> container.resolve(Client)
        Client(dep=<punq.AlternativeDependency object at 0x...>)
    """
    ...

class Scope(Enum):
    """
    Controls the lifetime of resolved objects.

    Attributes:
        transient: create a fresh instance for each `resolve` call
        singleton: re-use a single instance for every `resolve` call
    """
    transient = 0
    singleton = 1

_T = TypeVar("_T", default=Any)

class _Registration(NamedTuple, Generic[_T]):
    """_Registration(service, scope, builder, needs, args)"""
    service: type[_T] | str
    scope: Scope
    builder: Callable[..., _T]
    needs: dict[str, Any]  # the type hints of the builder's parameters
    args: dict[str, Any]  # passed to builder at instantiation time

_Empty = NewType("_Empty", object)  # a class at runtime
empty: Final[_Empty]

class _Registry:
    def register_service_and_impl(
        self,
        service: type[_T] | str,
        scope: Scope,
        impl: type[_T],
        resolve_args: dict[str, Any],  # forwarded to _Registration.builder
    ) -> None:
        """
        Registers a concrete implementation of an abstract service.

        Examples:
             In this example, the EmailSender type is an abstract class
             and SmtpEmailSender is our concrete implementation.

             >>> from punq import Container
             >>> container = Container()

             >>> class EmailSender:
             ...     def send(self, msg):
             ...         pass
             ...
             >>> class SmtpEmailSender(EmailSender):
             ...     def send(self, msg):
             ...         print("Sending message via smtp: " + msg)
             ...
             >>> container.register(EmailSender, SmtpEmailSender)
             <punq.Container object at 0x...>
             >>> instance = container.resolve(EmailSender)
             >>> instance.send("Hello")
             Sending message via smtp: Hello
        """
        ...
    def register_service_and_instance(self, service: type[_T] | str, instance: _T) -> None:
        """
        Register a singleton instance to implement a service.

        Examples:
            If we have an object that is expensive to construct, or that
            wraps a resource that must not be shared, we might choose to
            use a singleton instance.

            >>> import sqlalchemy
            >>> from punq import Container
            >>> container = Container()

            >>> class DataAccessLayer:
            ...     pass
            ...
            >>> class SqlAlchemyDataAccessLayer(DataAccessLayer):
            ...     def __init__(self, engine: sqlalchemy.engine.Engine):
            ...         pass
            ...
            >>> container.register(
            ...     DataAccessLayer,
            ...     instance=SqlAlchemyDataAccessLayer(
            ...         sqlalchemy.create_engine("sqlite:///"))
            ... )
            <punq.Container object at 0x...>
        """
        ...
    def register_concrete_service(self, service: type | str, scope: Scope) -> None:
        """
        Register a service as its own implementation.

        Examples:
            If we need to register a dependency, but we don't need to
            abstract it, we can register it as concrete.

            >>> from punq import Container
            >>> container = Container()
            >>> class FileReader:
            ...     def read(self):
            ...         # Assorted legerdemain and rigmarole
            ...         pass
            ...
            >>> container.register(FileReader)
            <punq.Container object at 0x...>
        """
        ...
    def build_context(self, key: type | str, existing: _ResolutionContext | None = None) -> _ResolutionContext: ...
    def register(
        self,
        service: type[_T] | str,
        factory: Callable[..., _T] | _Empty = ...,
        instance: _T | _Empty = ...,
        scope: Scope = Scope.transient,
        **kwargs: Any,  # forwarded to _Registration.builder
    ) -> None: ...
    def __getitem__(self, service: type[_T] | str) -> list[_Registration[_T]]: ...

class _ResolutionTarget(Generic[_T]):
    service: type[_T] | str
    impls: list[_Registration[_T]]
    def __init__(self, key: type[_T] | str, impls: list[_Registration[_T]]) -> None: ...
    def is_generic_list(self) -> bool: ...
    @property
    def generic_parameter(self) -> Any: ...  # returns the first annotated generic parameter of the service
    def next_impl(self) -> _Registration[_T]: ...

class _ResolutionContext:
    targets: dict[type | str, _ResolutionTarget[Any]]
    cache: dict[type | str, Any]  # resolved objects during this resolution
    service: type | str
    def __init__(self, key: type | str, impls: list[_Registration[Any]]) -> None: ...
    def target(self, key: type[_T] | str) -> _ResolutionTarget[_T]: ...
    def has_cached(self, key: type | str) -> bool: ...
    def __getitem__(self, key: type[_T] | str) -> _T: ...
    def __setitem__(self, key: type[_T] | str, value: _T) -> None: ...
    def all_registrations(self, service: type[_T] | str) -> list[_Registration[_T]]: ...

class Container:
    """
    Provides dependency registration and resolution.

    This is the main entrypoint of the Punq library. In normal scenarios users
    will only need to interact with this class.
    """
    registrations: _Registry
    def __init__(self) -> None: ...

    # all kwargs are forwarded to _Registration.builder
    @overload
    def register(self, service: type[_T] | str, *, instance: _T, **kwargs: Any) -> Container:
        """
        Register a dependency into the container.

        Each registration in Punq has a "service", which is the key used for
        resolving dependencies, and either an "instance" that implements the
        service or a "factory" that understands how to create an instance on
        demand.

        Examples:
            If we have an object that is expensive to construct, or that
            wraps a resouce that must not be shared, we might choose to
            use a singleton instance.

            >>> import sqlalchemy
            >>> from punq import Container
            >>> container = Container()

            >>> class DataAccessLayer:
            ...     pass
            ...
            >>> class SqlAlchemyDataAccessLayer(DataAccessLayer):
            ...     def __init__(self, engine: sqlalchemy.engine.Engine):
            ...         pass
            ...
            >>> dal = SqlAlchemyDataAccessLayer(sqlalchemy.create_engine("sqlite:///"))
            >>> container.register(
            ...     DataAccessLayer,
            ...     instance=dal
            ... )
            <punq.Container object at 0x...>
            >>> assert container.resolve(DataAccessLayer) is dal

            If we need to register a dependency, but we don't need to
                abstract it, we can register it as concrete.

            >>> class FileReader:
            ...     def read (self):
            ...         # Assorted legerdemain and rigmarole
            ...         pass
            ...
            >>> container.register(FileReader)
            <punq.Container object at 0x...>
            >>> assert type(container.resolve(FileReader)) == FileReader

            In this example, the EmailSender type is an abstract class
            and SmtpEmailSender is our concrete implementation.

            >>> class EmailSender:
            ...     def send(self, msg):
            ...         pass
            ...
            >>> class SmtpEmailSender (EmailSender):
            ...     def send(self, msg):
            ...         print("Sending message via smtp")
            ...
            >>> container.register(EmailSender, SmtpEmailSender)
            <punq.Container object at 0x...>
            >>> instance = container.resolve(EmailSender)
            >>> instance.send("beep")
            Sending message via smtp
        """
        ...
    @overload
    def register(
        self, service: type[_T] | str, factory: Callable[..., _T] | _Empty = ..., *, scope: Scope = Scope.transient, **kwargs: Any
    ) -> Container:
        """
        Register a dependency into the container.

        Each registration in Punq has a "service", which is the key used for
        resolving dependencies, and either an "instance" that implements the
        service or a "factory" that understands how to create an instance on
        demand.

        Examples:
            If we have an object that is expensive to construct, or that
            wraps a resouce that must not be shared, we might choose to
            use a singleton instance.

            >>> import sqlalchemy
            >>> from punq import Container
            >>> container = Container()

            >>> class DataAccessLayer:
            ...     pass
            ...
            >>> class SqlAlchemyDataAccessLayer(DataAccessLayer):
            ...     def __init__(self, engine: sqlalchemy.engine.Engine):
            ...         pass
            ...
            >>> dal = SqlAlchemyDataAccessLayer(sqlalchemy.create_engine("sqlite:///"))
            >>> container.register(
            ...     DataAccessLayer,
            ...     instance=dal
            ... )
            <punq.Container object at 0x...>
            >>> assert container.resolve(DataAccessLayer) is dal

            If we need to register a dependency, but we don't need to
                abstract it, we can register it as concrete.

            >>> class FileReader:
            ...     def read (self):
            ...         # Assorted legerdemain and rigmarole
            ...         pass
            ...
            >>> container.register(FileReader)
            <punq.Container object at 0x...>
            >>> assert type(container.resolve(FileReader)) == FileReader

            In this example, the EmailSender type is an abstract class
            and SmtpEmailSender is our concrete implementation.

            >>> class EmailSender:
            ...     def send(self, msg):
            ...         pass
            ...
            >>> class SmtpEmailSender (EmailSender):
            ...     def send(self, msg):
            ...         print("Sending message via smtp")
            ...
            >>> container.register(EmailSender, SmtpEmailSender)
            <punq.Container object at 0x...>
            >>> instance = container.resolve(EmailSender)
            >>> instance.send("beep")
            Sending message via smtp
        """
        ...
    @overload
    def register(
        self,
        service: type[_T] | str,
        factory: Callable[..., _T] | _Empty = ...,
        instance: _T | _Empty = ...,
        scope: Scope = Scope.transient,
        **kwargs: Any,
    ) -> Container:
        """
        Register a dependency into the container.

        Each registration in Punq has a "service", which is the key used for
        resolving dependencies, and either an "instance" that implements the
        service or a "factory" that understands how to create an instance on
        demand.

        Examples:
            If we have an object that is expensive to construct, or that
            wraps a resouce that must not be shared, we might choose to
            use a singleton instance.

            >>> import sqlalchemy
            >>> from punq import Container
            >>> container = Container()

            >>> class DataAccessLayer:
            ...     pass
            ...
            >>> class SqlAlchemyDataAccessLayer(DataAccessLayer):
            ...     def __init__(self, engine: sqlalchemy.engine.Engine):
            ...         pass
            ...
            >>> dal = SqlAlchemyDataAccessLayer(sqlalchemy.create_engine("sqlite:///"))
            >>> container.register(
            ...     DataAccessLayer,
            ...     instance=dal
            ... )
            <punq.Container object at 0x...>
            >>> assert container.resolve(DataAccessLayer) is dal

            If we need to register a dependency, but we don't need to
                abstract it, we can register it as concrete.

            >>> class FileReader:
            ...     def read (self):
            ...         # Assorted legerdemain and rigmarole
            ...         pass
            ...
            >>> container.register(FileReader)
            <punq.Container object at 0x...>
            >>> assert type(container.resolve(FileReader)) == FileReader

            In this example, the EmailSender type is an abstract class
            and SmtpEmailSender is our concrete implementation.

            >>> class EmailSender:
            ...     def send(self, msg):
            ...         pass
            ...
            >>> class SmtpEmailSender (EmailSender):
            ...     def send(self, msg):
            ...         print("Sending message via smtp")
            ...
            >>> container.register(EmailSender, SmtpEmailSender)
            <punq.Container object at 0x...>
            >>> instance = container.resolve(EmailSender)
            >>> instance.send("beep")
            Sending message via smtp
        """
        ...

    def resolve_all(self, service: type[_T] | str, **kwargs: Any) -> list[_T]:
        """
        Return all registrations for a given service.

        Some patterns require us to use multiple implementations of an
        interface at the same time.

        Examples:
            In this example, we want to use multiple Authenticator instances to
            check a request.

            >>> class Authenticator:
            ...     def matches(self, req):
            ...         return False
            ...
            ...     def authenticate(self, req):
            ...         return False
            ...
            >>> class BasicAuthenticator(Authenticator):
            ...     def matches(self, req):
            ...         head = req.headers.get("Authorization", "")
            ...         return head.startswith("Basic ")
            ...
            >>> class TokenAuthenticator(Authenticator):
            ...     def matches(self, req):
            ...         head = req.headers.get("Authorization", "")
            ...         return head.startswith("Bearer ")
            ...
            >>> def authenticate_request(container, req):
            ...     for authn in req.resolve_all(Authenticator):
            ...         if authn.matches(req):
            ...             return authn.authenticate(req)
        """
        ...
    def resolve(self, service_key: type[_T] | str, **kwargs: Any) -> _T:
        """Build an return an instance of a registered service."""
        ...
    def instantiate(self, service_key: type[_T] | str, **kwargs: Any) -> _T:
        """Instantiate an unregistered service."""
        ...
