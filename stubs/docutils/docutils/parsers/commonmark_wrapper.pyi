"""
An interface for parsing CommonMark input.

Select a locally installed parser from the following 3rd-party
parser packages:

:pycmark:       https://pypi.org/project/pycmark/
:myst:          https://pypi.org/project/myst-docutils/
:recommonmark:  https://pypi.org/project/recommonmark/ (deprecated)

The first parser class that can be successfully imported is mapped to
`commonmark_wrapper.Parser`.

This module is provisional:
the API is not settled and may change with any minor Docutils version.
"""

from typing import Literal, TypeAlias

from docutils import parsers

_ParserName: TypeAlias = Literal["pycmark", "myst", "recommonmark"]

commonmark_parser_names: tuple[_ParserName, ...]
Parser: type[parsers.Parser]  # if Parser is None or parser_name is empty string, user cannot import current module
parser_name: _ParserName
