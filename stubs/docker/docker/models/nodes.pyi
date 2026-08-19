from builtins import list as _list
from typing import Any, Literal

from .resource import Collection, Model

class Node(Model):
    """A node in a swarm."""
    id_attribute: str
    @property
    def version(self) -> int: ...
    def update(self, node_spec) -> Literal[True]: ...
    def remove(self, force: bool = False) -> Literal[True]: ...

class NodeCollection(Collection[Node]):
    """Nodes on the Docker server."""
    model: type[Node]
    def get(self, node_id) -> Node: ...
    # Please keep in sync with docker.api.swarm.SwarmApiMixin.nodes
    def list(self, filters: dict[str, Any] | None = None) -> _list[Node]:
        """
        List swarm nodes.

        Args:
            filters (dict): Filters to process on the nodes list. Valid
                filters: ``id``, ``name``, ``membership`` and ``role``.
                Default: ``None``

        Returns:
            A list of :py:class:`Node` objects.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> client.nodes.list(filters={'role': 'manager'})
        """
        ...
