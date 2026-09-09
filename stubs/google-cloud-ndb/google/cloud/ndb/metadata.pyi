"""
Models and helper functions for access to a project's datastore metadata.

These entities cannot be created by users, but are created as the results of
__namespace__, __kind__, __property__ and __entity_group__ metadata queries
or gets.

A simplified API is also offered:

    :func:`get_namespaces`: A list of namespace names.

    :func:`get_kinds`: A list of kind names.

    :func:`get_properties_of_kind`: A list of property names
    for the given kind name.

    :func:`get_representations_of_kind`: A dict mapping
    property names to lists of representation ids.

    get_kinds(), get_properties_of_kind(), get_representations_of_kind()
    implicitly apply to the current namespace.

    get_namespaces(), get_kinds(), get_properties_of_kind(),
    get_representations_of_kind() have optional start and end arguments to
    limit the query to a range of names, such that start <= name < end.
"""

from _typeshed import Incomplete

from google.cloud.ndb import model

class _BaseMetadata(model.Model):
    """Base class for all metadata models."""
    KIND_NAME: str
    def __new__(cls, *args, **kwargs):
        """override to prevent instantiation"""
        ...

class Namespace(_BaseMetadata):
    """Model for __namespace__ metadata query results."""
    KIND_NAME: str
    EMPTY_NAMESPACE_ID: int
    @property
    def namespace_name(self):
        """
        Return the namespace name specified by this entity's key.

        Returns:
            str: the namespace name.
        """
        ...
    @classmethod
    def key_for_namespace(cls, namespace):
        """
        Return the Key for a namespace.

        Args:
            namespace (str): A string giving the namespace whose key is
                requested.

        Returns:
            key.Key: The Key for the namespace.
        """
        ...
    @classmethod
    def key_to_namespace(cls, key):
        """
        Return the namespace specified by a given __namespace__ key.

        Args:
            key (key.Key): key whose name is requested.

        Returns:
            str: The namespace specified by key.
        """
        ...

class Kind(_BaseMetadata):
    """Model for __kind__ metadata query results."""
    KIND_NAME: str
    @property
    def kind_name(self):
        """
        Return the kind name specified by this entity's key.

        Returns:
            str: the kind name.
        """
        ...
    @classmethod
    def key_for_kind(cls, kind):
        """
        Return the __kind__ key for kind.

        Args:
            kind (str): kind whose key is requested.

        Returns:
            key.Key: key for kind.
        """
        ...
    @classmethod
    def key_to_kind(cls, key):
        """
        Return the kind specified by a given __kind__ key.

        Args:
            key (key.Key): key whose name is requested.

        Returns:
            str: The kind specified by key.
        """
        ...

class Property(_BaseMetadata):
    """Model for __property__ metadata query results."""
    KIND_NAME: str
    @property
    def property_name(self):
        """
        Return the property name specified by this entity's key.

        Returns:
            str: the property name.
        """
        ...
    @property
    def kind_name(self):
        """
        Return the kind name specified by this entity's key.

        Returns:
            str: the kind name.
        """
        ...
    property_representation: Incomplete
    @classmethod
    def key_for_kind(cls, kind):
        """
        Return the __property__ key for kind.

        Args:
            kind (str): kind whose key is requested.

        Returns:
            key.Key: The parent key for __property__ keys of kind.
        """
        ...
    @classmethod
    def key_for_property(cls, kind, property):
        """
        Return the __property__ key for property of kind.

        Args:
            kind (str): kind whose key is requested.
            property (str): property whose key is requested.

        Returns:
            key.Key: The key for property of kind.
        """
        ...
    @classmethod
    def key_to_kind(cls, key):
        """
        Return the kind specified by a given __property__ key.

        Args:
            key (key.Key): key whose kind name is requested.

        Returns:
            str: The kind specified by key.
        """
        ...
    @classmethod
    def key_to_property(cls, key):
        """
        Return the property specified by a given __property__ key.

        Args:
            key (key.Key): key whose property name is requested.

        Returns:
            str: property specified by key, or None if the key specified
                only a kind.
        """
        ...

class EntityGroup:
    """Model for __entity_group__ metadata. No longer supported by datastore."""
    def __new__(cls, *args, **kwargs): ...

def get_entity_group_version(*args, **kwargs) -> None: ...
def get_kinds(start=None, end=None): ...
def get_namespaces(start=None, end=None): ...
def get_properties_of_kind(kind, start=None, end=None): ...
def get_representations_of_kind(kind, start=None, end=None): ...
