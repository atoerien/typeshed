import re
from _typeshed import Incomplete
from itertools import chain
from typing import Final, overload

from dateparser.conf import Settings

PARSER_HARDCODED_TOKENS: Final[list[str]]
PARSER_KNOWN_TOKENS: Final[list[str]]
ALWAYS_KEEP_TOKENS: Final[list[str]]
KNOWN_WORD_TOKENS: Final[list[str]]
PARENTHESES_PATTERN: Final[re.Pattern[str]]
NUMERAL_PATTERN: Final[re.Pattern[str]]
KEEP_TOKEN_PATTERN: Final[re.Pattern[str]]

class UnknownTokenError(Exception): ...

class Dictionary:
    """
    Class that modifies and stores translations and handles splitting of date string.

    :param locale_info:
        Locale info (translation data) of the locale.
    :type language_info: dict

    :param settings:
        Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
    :type settings: dict

    :return: a Dictionary instance.
    """
    info: dict[str, Incomplete]
    def __init__(self, locale_info: dict[str, Incomplete], settings: Settings | None = None) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str): ...
    def __iter__(self) -> chain[str]: ...
    def are_tokens_valid(self, tokens: list[str]) -> bool:
        """
        Check if tokens are valid tokens for the locale.

        :param tokens:
            a list of string tokens.
        :type tokens: list

        :return: True if tokens are valid, False otherwise.
        """
        ...
    @overload
    def split(self, string: None, keep_formatting: bool = False) -> None:
        """
        Split the date string using translations in locale info.

        :param string:
            Date string to be splitted.
        :type string:
            str

        :param keep_formatting:
            If True, retain formatting of the date string.
        :type keep_formatting: bool

        :return: A list of string tokens formed after splitting the date string.
        """
        ...
    @overload
    def split(self, string: str, keep_formatting: bool = False) -> list[str]:
        """
        Split the date string using translations in locale info.

        :param string:
            Date string to be splitted.
        :type string:
            str

        :param keep_formatting:
            If True, retain formatting of the date string.
        :type keep_formatting: bool

        :return: A list of string tokens formed after splitting the date string.
        """
        ...

class NormalizedDictionary(Dictionary):
    def __init__(self, locale_info: dict[str, Incomplete], settings: Settings | None = None) -> None: ...
