"""All major API points and command-line tools"""

from argparse import ArgumentParser
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, TypeAlias, overload

from xmldiff.actions import (
    DeleteAttrib,
    DeleteNamespace,
    DeleteNode,
    InsertAttrib,
    InsertComment,
    InsertNamespace,
    InsertNode,
    MoveNode,
    RenameAttrib,
    RenameNode,
    UpdateAttrib,
    UpdateTextAfter,
    UpdateTextIn,
)
from xmldiff.formatting import BaseFormatter

__version__: str
FORMATTERS: Mapping[str, BaseFormatter]

_ACTIONS: TypeAlias = (
    DeleteNode
    | InsertNode
    | RenameNode
    | MoveNode
    | UpdateTextIn
    | UpdateTextAfter
    | UpdateAttrib
    | DeleteAttrib
    | InsertAttrib
    | RenameAttrib
    | InsertComment
    | InsertNamespace
    | DeleteNamespace
)
_ET: TypeAlias = Any  # lxml.etree._ElementTree

@overload
def diff_trees(left: _ET, right: _ET, *, diff_options: dict[str, Any] | None = None, formatter: BaseFormatter) -> str:
    """Takes two lxml root elements or element trees"""
    ...
@overload
def diff_trees(
    left: _ET, right: _ET, diff_options: dict[str, Any] | None = None, formatter: None = None
) -> Iterable[_ACTIONS]:
    """Takes two lxml root elements or element trees"""
    ...
@overload
def diff_texts(
    left: str | bytes, right: str | bytes, *, diff_options: dict[str, Any] | None = None, formatter: BaseFormatter
) -> str:
    """Takes two Unicode strings containing XML"""
    ...
@overload
def diff_texts(
    left: str | bytes, right: str | bytes, diff_options: dict[str, Any] | None = None, formatter: None = None
) -> Iterable[_ACTIONS]:
    """Takes two Unicode strings containing XML"""
    ...
@overload
def diff_files(left: str, right: str, *, diff_options: dict[str, Any] | None = None, formatter: BaseFormatter) -> str:
    """Takes two filenames or streams, and diffs the XML in those files"""
    ...
@overload
def diff_files(
    left: str, right: str, diff_options: dict[str, Any] | None = None, formatter: None = None
) -> Iterable[_ACTIONS]:
    """Takes two filenames or streams, and diffs the XML in those files"""
    ...
def validate_F(arg: float | str) -> float:
    """Type function for argparse - a float within some predefined bounds"""
    ...
def make_diff_parser() -> ArgumentParser: ...
def diff_command(args: Sequence[str] | None = None) -> int | None: ...
def patch_tree(actions, tree):
    """Takes an lxml root element or element tree, and a list of actions"""
    ...
def patch_text(actions, tree):
    """Takes a string with XML and a string with actions"""
    ...
def patch_file(actions, tree, diff_encoding=None):
    """Takes two filenames or streams, one with XML the other a diff"""
    ...
def make_patch_parser(): ...
def patch_command(args=None) -> None: ...
