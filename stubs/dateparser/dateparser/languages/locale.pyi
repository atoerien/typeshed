from _typeshed import Incomplete
from collections import OrderedDict
from collections.abc import Mapping, Sized
from re import Pattern
from typing import Final, TypeVar

from dateparser.conf import Settings

_K = TypeVar("_K", bound=Sized)
_V = TypeVar("_V")

NUMERAL_PATTERN: Final[Pattern[str]]

class Locale:
    """
    Class that deals with applicability and translation from a locale.

    :param shortname:
        A locale code, e.g. 'fr-PF', 'qu-EC', 'af-NA'.
    :type shortname: str

    :param language_info:
        Language info (translation data) of the language the locale belongs to.
    :type language_info: dict

    :return: A Locale instance
    """
    shortname: str
    info: OrderedDict[str, Incomplete]
    def __init__(self, shortname: str, language_info: Mapping[Incomplete, Incomplete]) -> None: ...
    def is_applicable(self, date_string: str, strip_timezone: bool = False, settings: Settings | None = None) -> bool:
        """
        Check if the locale is applicable to translate date string.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param strip_timezone:
            If True, timezone is stripped from date string.
        :type strip_timezone: bool

        :return: boolean value representing if the locale is applicable for the date string or not.
        """
        ...
    def count_applicability(self, text: str, strip_timezone: bool = False, settings: Settings | None = None) -> list[int]: ...
    @staticmethod
    def clean_dictionary(dictionary: Mapping[_K, _V], threshold: int = 2) -> Mapping[_K, _V]: ...
    def translate(self, date_string: str, keep_formatting: bool = False, settings: Settings | None = None) -> str:
        """
        Translate the date string to its English equivalent.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param keep_formatting:
            If True, retain formatting of the date string after translation.
        :type keep_formatting: bool

        :return: translated date string.
        """
        ...
    def translate_search(self, search_string: str, settings: Settings | None = None) -> tuple[list[str], list[str]]: ...
    def get_wordchars_for_detection(self, settings: Settings) -> set[str]: ...
    def to_parserinfo(self, base_cls: type = ...): ...
