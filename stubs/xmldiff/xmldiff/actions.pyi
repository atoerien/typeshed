from _typeshed import Incomplete
from typing import NamedTuple

class DeleteNode(NamedTuple):
    """DeleteNode(node,)"""
    node: str

class InsertNode(NamedTuple):
    """InsertNode(target, tag, position)"""
    target: Incomplete
    tag: str
    position: int

class RenameNode(NamedTuple):
    """RenameNode(node, tag)"""
    node: str
    tag: Incomplete

class MoveNode(NamedTuple):
    """MoveNode(node, target, position)"""
    node: str
    target: Incomplete
    position: int

class UpdateTextIn(NamedTuple):
    """UpdateTextIn(node, text)"""
    node: str
    text: Incomplete
    oldtext: Incomplete | None = None

class UpdateTextAfter(NamedTuple):
    """UpdateTextAfter(node, text)"""
    node: str
    text: Incomplete
    oldtext: Incomplete | None = None

class UpdateAttrib(NamedTuple):
    """UpdateAttrib(node, name, value)"""
    node: str
    name: str
    value: Incomplete

class DeleteAttrib(NamedTuple):
    """DeleteAttrib(node, name)"""
    node: str
    name: str

class InsertAttrib(NamedTuple):
    """InsertAttrib(node, name, value)"""
    node: str
    name: str
    value: Incomplete

class RenameAttrib(NamedTuple):
    """RenameAttrib(node, oldname, newname)"""
    node: str
    oldname: str
    newname: str

class InsertComment(NamedTuple):
    """InsertComment(target, position, text)"""
    target: Incomplete
    position: Incomplete
    text: Incomplete

class InsertNamespace(NamedTuple):
    """InsertNamespace(prefix, uri)"""
    prefix: str
    uri: str

class DeleteNamespace(NamedTuple):
    """DeleteNamespace(prefix,)"""
    prefix: str
