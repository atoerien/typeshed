"""Utility functions to position and resize boxes within boxes"""

from _typeshed import Incomplete
from typing import Final, Literal, overload

__version__: Final[str]

@overload
def rectCorner(
    x, y, width, height, anchor: str = "sw", dims: Literal[True] = ...
) -> tuple[Incomplete, Incomplete, Incomplete, Incomplete]:
    """
    given rectangle controlled by x,y width and height return 
    the corner corresponding to the anchor
    """
    ...
@overload
def rectCorner(x, y, width, height, anchor: str = "sw", dims: Literal[False] | None = False) -> tuple[Incomplete, Incomplete]:
    """
    given rectangle controlled by x,y width and height return 
    the corner corresponding to the anchor
    """
    ...
def aspectRatioFix(
    preserve, anchor, x, y, width, height, imWidth, imHeight, anchorAtXY: bool = False
) -> tuple[Incomplete, Incomplete, Incomplete, Incomplete, Incomplete]:
    """
    This function helps position an image within a box.

    It first normalizes for two cases:
    - if the width is None, it assumes imWidth
    - ditto for height
    - if width or height is negative, it adjusts x or y and makes them positive

    Given
    (a) the enclosing box (defined by x,y,width,height where x,y is the         lower left corner) which you wish to position the image in, and
    (b) the image size (imWidth, imHeight), and
    (c) the 'anchor point' as a point of the compass - n,s,e,w,ne,se etc         and c for centre,

    this should return the position at which the image should be drawn,
    as well as a scale factor indicating what scaling has happened.

    It returns the parameters which would be used to draw the image
    without any adjustments:

        x,y, width, height, scale

    used in canvas.drawImage and drawInlineImage
    """
    ...
