"""helper for importing pdf structures into a ReportLab generated document"""

from _typeshed import Incomplete
from collections.abc import Iterator
from typing_extensions import Self

from reportlab.pdfbase.pdfdoc import PDFObject

class PDFPattern(PDFObject):
    __RefOnly__: int
    pattern: Incomplete
    arguments: dict[str, Incomplete]
    def __init__(self, pattern_sequence, **keywordargs) -> None: ...
    def __setitem__(self, item: str, value) -> None: ...
    def __getitem__(self, item: str): ...
    def eval(self, L) -> Iterator[bytes]: ...
    def format(self, document) -> bytes: ...
    def clone(self) -> Self: ...

class PDFPatternIf:
    """
    cond will be evaluated as [cond] in PDFpattern eval.
    It should evaluate to a list with value 0/1 etc etc.
    thenPart is a list to be evaluated if the cond evaulates true,
    elsePart is the false sequence.
    """
    cond: Incomplete
    thenPart: Incomplete
    elsePart: Incomplete
    def __init__(self, cond, thenPart=[], elsePart=[]) -> None: ...
