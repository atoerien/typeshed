'This module defines standard interpreted text role functions, a registry for\ninterpreted text roles, and an API for adding to and retrieving from the\nregistry. See also `Creating reStructuredText Interpreted Text Roles`__.\n\n__ https://docutils.sourceforge.io/docs/ref/rst/roles.html\n\n\nThe interface for interpreted role functions is as follows::\n\n    def role_fn(name, rawtext, text, lineno, inliner,\n                options=None, content=None):\n        code...\n\n    # Set function attributes for customization:\n    role_fn.options = ...\n    role_fn.content = ...\n\nParameters:\n\n- ``name`` is the local name of the interpreted text role, the role name\n  actually used in the document.\n\n- ``rawtext`` is a string containing the entire interpreted text construct.\n  Return it as a ``problematic`` node linked to a system message if there is a\n  problem.\n\n- ``text`` is the interpreted text content, with backslash escapes converted\n  to nulls (``\x00``).\n\n- ``lineno`` is the line number where the text block containing the\n  interpreted text begins.\n\n- ``inliner`` is the Inliner object that called the role function.\n  It defines the following useful attributes: ``reporter``,\n  ``problematic``, ``memo``, ``parent``, ``document``.\n\n- ``options``: A dictionary of directive options for customization, to be\n  interpreted by the role function.  Used for additional attributes for the\n  generated elements and other functionality.\n\n- ``content``: A list of strings, the directive content for customization\n  ("role" directive).  To be interpreted by the role function.\n\nFunction attributes for customization, interpreted by the "role" directive:\n\n- ``options``: A dictionary, mapping known option names to conversion\n  functions such as `int` or `float`.  ``None`` or an empty dict implies no\n  options to parse.  Several directive option conversion functions are defined\n  in the `directives` module.\n\n  All role functions implicitly support the "class" option, unless disabled\n  with an explicit ``{\'class\': None}``.\n\n- ``content``: A boolean; true if content is allowed.  Client code must handle\n  the case where content is required but not supplied (an empty content list\n  will be supplied).\n\nNote that unlike directives, the "arguments" function attribute is not\nsupported for role customization.  Directive arguments are handled by the\n"role" directive itself.\n\nInterpreted role functions return a tuple of two values:\n\n- A list of nodes which will be inserted into the document tree at the\n  point where the interpreted role was encountered (can be an empty\n  list).\n\n- A list of system messages, which will be inserted into the document tree\n  immediately after the end of the current inline block (can also be empty).'

from collections.abc import Callable, Mapping, Sequence
from typing import Any, Final, TypeAlias
from typing_extensions import deprecated

import docutils.parsers.rst.states
from docutils import nodes
from docutils.languages import _LanguageModule
from docutils.nodes import Node, system_message
from docutils.parsers.rst.states import Inliner
from docutils.utils import Reporter

__docformat__: Final = "reStructuredText"
DEFAULT_INTERPRETED_ROLE: Final = "title-reference"

_RoleFn: TypeAlias = Callable[
    [str, str, str, int, docutils.parsers.rst.states.Inliner, Mapping[str, Any], Sequence[str]],
    tuple[Sequence[nodes.reference], Sequence[nodes.reference]],
]

def register_canonical_role(name: str, role_fn: _RoleFn) -> None:
    """
    Register an interpreted text role by its canonical name.

    :Parameters:
      - `name`: The canonical name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """
    ...
def register_local_role(name: str, role_fn: _RoleFn) -> None:
    """
    Register an interpreted text role by its local or language-dependent name.

    :Parameters:
      - `name`: The local or language-dependent name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """
    ...
def role(
    role_name: str, language_module: _LanguageModule, lineno: int, reporter: Reporter
) -> tuple[_RoleFn | None, list[system_message]]:
    """
    Locate and return a role function from its language-dependent name, along
    with a list of system messages.

    If the role is not found in the current language, check English. Return a
    2-tuple: role function (``None`` if the named role cannot be found) and a
    list of system messages.
    """
    ...
def set_implicit_options(role_fn: _RoleFn) -> None:
    """
    Add customization options to role functions, unless explicitly set or
    disabled.
    """
    ...
def register_generic_role(canonical_name: str, node_class: type[Node]) -> None:
    """For roles which simply wrap a given `node_class` around the text."""
    ...

class GenericRole:
    """
    Generic interpreted text role.

    The interpreted text is simply wrapped with the provided node class.
    """
    name: str
    node_class: type[Node]
    def __init__(self, role_name: str, node_class: type[Node]) -> None: ...
    def __call__(
        self,
        role: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> tuple[list[Node], list[system_message]]: ...

class CustomRole:
    """Wrapper for custom interpreted text roles."""
    name: str
    base_role: _RoleFn | CustomRole
    options: Mapping[str, Any]
    content: Sequence[str]
    supplied_options: Mapping[str, Any]
    supplied_content: Sequence[str]
    def __init__(
        self,
        role_name: str,
        base_role: _RoleFn | CustomRole,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> None: ...
    def __call__(
        self,
        role: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> tuple[list[Node], list[system_message]]: ...

def generic_custom_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]:
    """Base for custom roles if no other base role is specified."""
    ...
def pep_reference_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def rfc_reference_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def raw_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def code_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def math_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def unimplemented_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
@deprecated("Deprecated and will be removed in Docutils 2.0, Use `roles.normalize_options()` instead.")
def set_classes(options: dict[str, str]) -> None:
    """Deprecated. Obsoleted by ``normalize_options()``."""
    ...
@deprecated("Deprecated and will be removed in Docutils 2.0, Use `roles.normalize_options()` instead.")
def normalized_role_options(options: Mapping[str, Any] | None) -> dict[str, Any]: ...
def normalize_options(options: Mapping[str, Any] | None) -> dict[str, Any]:
    """
    Return normalized dictionary of role/directive options.

    * ``None`` is replaced by an empty dictionary.
    * The key 'class' is renamed to 'classes'.
    """
    ...
