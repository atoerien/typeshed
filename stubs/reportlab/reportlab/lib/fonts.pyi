from typing import Final, Literal, TypeAlias

_BoolInt: TypeAlias = Literal[0, 1]

__version__: Final[str]

def ps2tt(psfn: str) -> tuple[str, _BoolInt, _BoolInt]:
    """ps fontname to family name, bold, italic"""
    ...
def tt2ps(fn: str, b: _BoolInt, i: _BoolInt) -> str:
    """family name + bold & italic to ps font name"""
    ...
def addMapping(face: str, bold: _BoolInt, italic: _BoolInt, psname: str) -> None:
    """allow a custom font to be put in the mapping"""
    ...
