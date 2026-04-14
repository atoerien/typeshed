from .ast import Node

def parse_component_value_list(css: str, skip_comments: bool = False) -> list[Node]:
    """
    Parse a list of component values.

    :type css: :obj:`str`
    :param css: A CSS string.
    :type skip_comments: :obj:`bool`
    :param skip_comments:
        Ignore CSS comments.
        The return values (and recursively its blocks and functions)
        will not contain any :class:`~tinycss2.ast.Comment` object.
    :returns: A list of :term:`component values`.
    """
    ...
