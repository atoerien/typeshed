from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, Flag, IntEnum, IntFlag
from typing import Final, Literal, TypeAlias
from typing_extensions import Self

from .drawing import DeviceCMYK, DeviceGray, DeviceRGB
from .syntax import Name

_Color: TypeAlias = str | int | Sequence[int] | DeviceCMYK | DeviceGray | DeviceRGB

class SignatureFlag(IntEnum):
    """An enumeration."""
    SIGNATURES_EXIST = 1
    APPEND_ONLY = 2

class CoerciveEnum(Enum):  # type: ignore[misc]  # Enum with no members
    """An enumeration that provides a helper to coerce strings into enumeration members."""
    @classmethod
    def coerce(cls, value: Self | str, case_sensitive: bool = False) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it as an enumeration value. If
        that fails, attempt to convert it (case insensitively, by upcasing) as an
        enumeration name.

        If all different conversion attempts fail, an exception is raised.

        Args:
            value (Enum, str): the value to be coerced.

        Raises:
            ValueError: if `value` is a string but neither a member by name nor value.
            TypeError: if `value`'s type is neither a member of the enumeration nor a
                string.
        """
        ...

class CoerciveIntEnum(IntEnum):  # type: ignore[misc]  # Enum with no members
    """
    An enumeration that provides a helper to coerce strings and integers into
    enumeration members.
    """
    @classmethod
    def coerce(cls, value: Self | str | int) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it (case insensitively, by
        upcasing) as an enumeration name. Otherwise, if it is an int, attempt to
        convert it as an enumeration value.

        Otherwise, an exception is raised.

        Args:
            value (IntEnum, str, int): the value to be coerced.

        Raises:
            ValueError: if `value` is an int but not a member of this enumeration.
            ValueError: if `value` is a string but not a member by name.
            TypeError: if `value`'s type is neither a member of the enumeration nor an
                int or a string.
        """
        ...

class CoerciveIntFlag(IntFlag):  # type: ignore[misc]  # Enum with no members
    """
    Enumerated constants that can be combined using the bitwise operators,
    with a helper to coerce strings and integers into enumeration members.
    """
    @classmethod
    def coerce(cls, value: Self | str | int) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it (case insensitively, by
        upcasing) as an enumeration name. Otherwise, if it is an int, attempt to
        convert it as an enumeration value.
        Otherwise, an exception is raised.

        Args:
            value (IntEnum, str, int): the value to be coerced.

        Raises:
            ValueError: if `value` is an int but not a member of this enumeration.
            ValueError: if `value` is a string but not a member by name.
            TypeError: if `value`'s type is neither a member of the enumeration nor an
                int or a string.
        """
        ...

class WrapMode(CoerciveEnum):
    """Defines how to break and wrap lines in multi-line text."""
    WORD = "WORD"
    CHAR = "CHAR"

class CharVPos(CoerciveEnum):
    """Defines the vertical position of text relative to the line."""
    SUP = "SUP"
    SUB = "SUB"
    NOM = "NOM"
    DENOM = "DENOM"
    LINE = "LINE"

class Align(CoerciveEnum):
    """Defines how to render text in a cell"""
    C = "CENTER"
    X = "X_CENTER"
    L = "LEFT"
    R = "RIGHT"
    J = "JUSTIFY"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

_Align: TypeAlias = Align | Literal["CENTER", "X_CENTER", "LEFT", "RIGHT", "JUSTIFY"]  # noqa: Y047

class VAlign(CoerciveEnum):
    """
    Defines how to vertically render text in a cell.
    Default value is MIDDLE
    """
    M = "MIDDLE"
    T = "TOP"
    B = "BOTTOM"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class TextEmphasis(CoerciveIntFlag):
    """
    Indicates use of bold / italics / underline.

    This enum values can be combined with & and | operators:
        style = B | I
    """
    NONE = 0
    B = 1
    I = 2
    U = 4
    S = 8

    @property
    def style(self) -> str: ...
    def add(self, value: TextEmphasis) -> TextEmphasis: ...
    def remove(self, value: TextEmphasis) -> TextEmphasis: ...

class MethodReturnValue(CoerciveIntFlag):
    """
    Defines the return value(s) of a FPDF content-rendering method.

    This enum values can be combined with & and | operators:
        PAGE_BREAK | LINES
    """
    PAGE_BREAK = 1
    LINES = 2
    HEIGHT = 4

class CellBordersLayout(CoerciveIntFlag):
    """
    Defines how to render cell borders in table

    The integer value of `border` determines which borders are applied. Below are some common examples:

    - border=1 (LEFT): Only the left border is enabled.
    - border=3 (LEFT | RIGHT): Both the left and right borders are enabled.
    - border=5 (LEFT | TOP): The left and top borders are enabled.
    - border=12 (TOP | BOTTOM): The top and bottom borders are enabled.
    - border=15 (ALL): All borders (left, right, top, bottom) are enabled.
    - border=16 (INHERIT): Inherit the border settings from the parent element.

    Using `border=3` will combine LEFT and RIGHT borders, as it represents the
    bitwise OR of `LEFT (1)` and `RIGHT (2)`.
    """
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 4
    BOTTOM = 8
    ALL = 15
    INHERIT = 16

@dataclass
class TableBorderStyle:
    """
    A helper class for drawing one border of a table

    Attributes:
        thickness: The thickness of the border. If None use default. If <= 0 don't draw the border.
        color: The color of the border. If None use default.
    """
    thickness: float | None = None
    color: int | tuple[int, int, int] | None = None
    dash: float | None = None
    gap: float = 0.0
    phase: float = 0.0

    @staticmethod
    def from_bool(should_draw: TableBorderStyle | bool | None) -> TableBorderStyle:
        """From boolean or TableBorderStyle input, convert to definite TableBorderStyle class object"""
        ...
    @property
    def dash_dict(self) -> dict[str, float | None]:
        """Return dict object specifying dash in the same format as the pdf object"""
        ...
    def changes_stroke(self, pdf) -> bool:
        """Return True if this style changes the any aspect of the draw command, False otherwise"""
        ...
    def should_render(self) -> bool:
        """Return True if this style produces a visible stroke, False otherwise"""
        ...
    def get_change_stroke_commands(self, scale: float) -> list[str]:
        """Return list of strings for the draw command to change stroke (empty if no change)"""
        ...
    @staticmethod
    def get_line_command(x1: float, y1: float, x2: float, y2: float) -> list[str]:
        """Return list with string for the command to draw a line at the specified endpoints"""
        ...
    def get_draw_commands(self, pdf, x1: float, y1: float, x2: float, y2: float) -> list[str]:
        """
        Get draw commands for this section of a cell border. x and y are presumed to be already
        shifted and scaled.
        """
        ...

@dataclass
class TableCellStyle:
    """
    A helper class for drawing all the borders of one cell in a table

    Attributes:
        left: bool or TableBorderStyle specifying the style of the cell's left border
        bottom: bool or TableBorderStyle specifying the style of the cell's bottom border
        right: bool or TableBorderStyle specifying the style of the cell's right border
        top: bool or TableBorderStyle specifying the style of the cell's top border
    """
    left: bool | TableBorderStyle = False
    bottom: bool | TableBorderStyle = False
    right: bool | TableBorderStyle = False
    top: bool | TableBorderStyle = False

    @staticmethod
    def get_change_fill_color_command(color: _Color | None) -> list[str]:
        """Return list with string for command to change device color (empty list if no color)"""
        ...
    def get_draw_commands(
        self, pdf, x1: float, y1: float, x2: float, y2: float, fill_color: _Color | None = None
    ) -> list[str]:
        """
        Get list of primitive commands to draw the cell border for this cell, and fill it with the
        given fill color.
        """
        ...
    def override_cell_border(self, cell_border: CellBordersLayout) -> Self:
        """Allow override by CellBordersLayout mechanism"""
        ...
    def draw_cell_border(self, pdf, x1: float, y1: float, x2: float, y2: float, fill_color: _Color | None = None) -> None:
        """Draw the cell border for this cell, and fill it with the given fill color."""
        ...

class TableBordersLayout(ABC):
    """
    Customizable class for setting the drawing style of cell borders for the whole table.
    cell_style_getter is an abstract method that derived classes must implement. All current classes
    do not use self, but it is available in case a very complicated derived class needs to refer to
    stored internal data.

    Standard TableBordersLayouts are available as static members of this class

    Attributes:
        cell_style_getter: a callable that takes row_num, column_num,
            num_heading_rows, num_rows, num_columns; and returns the drawing style of
            the cell border (as a TableCellStyle object)
        ALL: static TableBordersLayout that draws all table cells borders
        NONE: static TableBordersLayout that draws no table cells borders
        INTERNAL: static TableBordersLayout that draws only internal horizontal & vertical borders
        MINIMAL: static TableBordersLayout that draws only the top horizontal border, below the
            headings, and internal vertical borders
        HORIZONTAL_LINES: static TableBordersLayout that draws only horizontal lines
        NO_HORIZONTAL_LINES: static TableBordersLayout that draws all cells border except interior
            horizontal lines after the headings
        SINGLE_TOP_LINE: static TableBordersLayout that draws only the top horizontal border, below
            the headings
    """
    ALL: Final[TableBordersLayoutAll]
    NONE: Final[TableBordersLayoutNone]
    INTERNAL: Final[TableBordersLayoutInternal]
    MINIMAL: Final[TableBordersLayoutMinimal]
    HORIZONTAL_LINES: Final[TableBordersLayoutHorizontalLines]
    NO_HORIZONTAL_LINES: Final[TableBordersLayoutNoHorizontalLines]
    SINGLE_TOP_LINE: Final[TableBordersLayoutSingleTopLine]
    @abstractmethod
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle:
        """
        Specify the desired TableCellStyle for the given position in the table

        Args:
            row_idx: the 0-based index of the row in the table
            col_idx: the 0-based logical index of the cell in the row. If colspan > 1, this indexes
                into non-null cells. e.g. if there are two cells with colspan = 3, then col_idx will
                be 0 or 1
            col_pos: the 0-based physical position of the cell in the row. If colspan > 1, this
                indexes into all cells including null ones. e.g. e.g. if there are two cells with
                colspan = 3, then col_pos will be 0 or 3
            num_heading_rows: the number of rows in the table heading
            num_rows: the total number of rows in the table
            num_col_idx: the number of non-null cells. e.g. if there are two cells with colspan = 3,
                then num_col_idx = 2
            num_col_pos: the full width of the table in physical cells. e.g. if there are two cells
                with colspan = 3, then num_col_pos = 6
        Returns:
            TableCellStyle for the given position in the table
        """
        ...
    @classmethod
    def coerce(cls, value: Self | str) -> Self:
        """
        Attempt to coerce `value` into a member of this class.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it as an enumeration value. If
        that fails, attempt to convert it (case insensitively, by upcasing) as an
        enumeration name.

        If all different conversion attempts fail, an exception is raised.

        Args:
            value (Enum, str): the value to be coerced.

        Raises:
            ValueError: if `value` is a string but neither a member by name nor value.
            TypeError: if `value`'s type is neither a member of the enumeration nor a
                string.
        """
        ...

class TableBordersLayoutAll(TableBordersLayout):
    """Class for drawing all cell borders"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutNone(TableBordersLayout):
    """Class for drawing zero cell borders"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutInternal(TableBordersLayout):
    """Class to draw only internal horizontal & vertical borders"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutMinimal(TableBordersLayout):
    """Class to draw only the top horizontal border, below the headings, and internal vertical borders"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutHorizontalLines(TableBordersLayout):
    """Class to draw only horizontal lines"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutNoHorizontalLines(TableBordersLayout):
    """Class to draw all cells border except interior horizontal lines after the headings"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableBordersLayoutSingleTopLine(TableBordersLayout):
    """Class to draw a single top line"""
    def cell_style_getter(
        self, row_idx: int, col_idx: int, col_pos: int, num_heading_rows: int, num_rows: int, num_col_idx: int, num_col_pos: int
    ) -> TableCellStyle: ...

class TableCellFillMode(CoerciveEnum):
    """Defines which table cells to fill"""
    NONE = "NONE"
    ALL = "ALL"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"
    EVEN_ROWS = "EVEN_ROWS"
    EVEN_COLUMNS = "EVEN_COLUMNS"

    def should_fill_cell(self, i: int, j: int) -> bool: ...
    @classmethod
    def coerce(cls, value: Self | str) -> Self:
        """Any class that has a .should_fill_cell() method is considered a valid 'TableCellFillMode' (duck-typing)"""
        ...

class TableSpan(CoerciveEnum):
    """An enumeration."""
    ROW = "ROW"
    COL = "COL"

class TableHeadingsDisplay(CoerciveIntEnum):
    """Defines how the table headings should be displayed"""
    NONE = 0
    ON_TOP_OF_EVERY_PAGE = 1

class RenderStyle(CoerciveEnum):
    """Defines how to render shapes"""
    D = "DRAW"
    F = "FILL"
    DF = "DRAW_FILL"
    @property
    def operator(self) -> str: ...
    @property
    def is_draw(self) -> bool: ...
    @property
    def is_fill(self) -> bool: ...
    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class TextMode(CoerciveIntEnum):
    """Values described in PDF spec section 'Text Rendering Mode'"""
    FILL = 0
    STROKE = 1
    FILL_STROKE = 2
    INVISIBLE = 3
    FILL_CLIP = 4
    STROKE_CLIP = 5
    FILL_STROKE_CLIP = 6
    CLIP = 7

class XPos(CoerciveEnum):
    """Positional values in horizontal direction for use after printing text."""
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    START = "START"
    END = "END"
    WCONT = "WCONT"
    CENTER = "CENTER"
    LMARGIN = "LMARGIN"
    RMARGIN = "RMARGIN"

class YPos(CoerciveEnum):
    """Positional values in vertical direction for use after printing text"""
    TOP = "TOP"
    LAST = "LAST"
    NEXT = "NEXT"
    TMARGIN = "TMARGIN"
    BMARGIN = "BMARGIN"

class Angle(CoerciveIntEnum):
    """Direction values used for mirror transformations specifying the angle of mirror line"""
    NORTH = 90
    EAST = 0
    SOUTH = 270
    WEST = 180
    NORTHEAST = 45
    SOUTHEAST = 315
    SOUTHWEST = 225
    NORTHWEST = 135

class PageLayout(CoerciveEnum):
    """Specify the page layout shall be used when the document is opened"""
    SINGLE_PAGE = Name("SinglePage")
    ONE_COLUMN = Name("OneColumn")
    TWO_COLUMN_LEFT = Name("TwoColumnLeft")
    TWO_COLUMN_RIGHT = Name("TwoColumnRight")
    TWO_PAGE_LEFT = Name("TwoPageLeft")
    TWO_PAGE_RIGHT = Name("TwoPageRight")

class PageMode(CoerciveEnum):
    """Specifying how to display the document on exiting full-screen mode"""
    USE_NONE = Name("UseNone")
    USE_OUTLINES = Name("UseOutlines")
    USE_THUMBS = Name("UseThumbs")
    FULL_SCREEN = Name("FullScreen")
    USE_OC = Name("UseOC")
    USE_ATTACHMENTS = Name("UseAttachments")

class TextMarkupType(CoerciveEnum):
    """Subtype of a text markup annotation"""
    HIGHLIGHT = Name("Highlight")
    UNDERLINE = Name("Underline")
    SQUIGGLY = Name("Squiggly")
    STRIKE_OUT = Name("StrikeOut")

class BlendMode(CoerciveEnum):
    """An enumeration of the named standard named blend functions supported by PDF."""
    NORMAL = Name("Normal")
    MULTIPLY = Name("Multiply")
    SCREEN = Name("Screen")
    OVERLAY = Name("Overlay")
    DARKEN = Name("Darken")
    LIGHTEN = Name("Lighten")
    COLOR_DODGE = Name("ColorDodge")
    COLOR_BURN = Name("ColorBurn")
    HARD_LIGHT = Name("HardLight")
    SOFT_LIGHT = Name("SoftLight")
    DIFFERENCE = Name("Difference")
    EXCLUSION = Name("Exclusion")
    HUE = Name("Hue")
    SATURATION = Name("Saturation")
    COLOR = Name("Color")
    LUMINOSITY = Name("Luminosity")

class AnnotationFlag(CoerciveIntEnum):
    """An enumeration."""
    INVISIBLE = 1
    HIDDEN = 2
    PRINT = 4
    NO_ZOOM = 8
    NO_ROTATE = 16
    NO_VIEW = 32
    READ_ONLY = 64
    LOCKED = 128
    TOGGLE_NO_VIEW = 256
    LOCKED_CONTENTS = 512

class AnnotationName(CoerciveEnum):
    """The name of an icon that shall be used in displaying the annotation"""
    NOTE = Name("Note")
    COMMENT = Name("Comment")
    HELP = Name("Help")
    PARAGRAPH = Name("Paragraph")
    NEW_PARAGRAPH = Name("NewParagraph")
    INSERT = Name("Insert")

class FileAttachmentAnnotationName(CoerciveEnum):
    """The name of an icon that shall be used in displaying the annotation"""
    PUSH_PIN = Name("PushPin")
    GRAPH_PUSH_PIN = Name("GraphPushPin")
    PAPERCLIP_TAG = Name("PaperclipTag")

class IntersectionRule(CoerciveEnum):
    """
    An enumeration representing the two possible PDF intersection rules.

    The intersection rule is used by the renderer to determine which points are
    considered to be inside the path and which points are outside the path. This
    primarily affects fill rendering and clipping paths.
    """
    NONZERO = "nonzero"
    EVENODD = "evenodd"

class PathPaintRule(CoerciveEnum):
    """
    An enumeration of the PDF drawing directives that determine how the renderer should
    paint a given path.
    """
    STROKE = "S"
    FILL_NONZERO = "f"
    FILL_EVENODD = "f*"
    STROKE_FILL_NONZERO = "B"
    STROKE_FILL_EVENODD = "B*"
    DONT_PAINT = "n"
    AUTO = "auto"

class ClippingPathIntersectionRule(CoerciveEnum):
    """An enumeration of the PDF drawing directives that define a path as a clipping path."""
    NONZERO = "W"
    EVENODD = "W*"

class StrokeCapStyle(CoerciveIntEnum):
    """
    An enumeration of values defining how the end of a stroke should be rendered.

    This affects the ends of the segments of dashed strokes, as well.
    """
    BUTT = 0
    ROUND = 1
    SQUARE = 2

class StrokeJoinStyle(CoerciveIntEnum):
    """
    An enumeration of values defining how the corner joining two path components should
    be rendered.
    """
    MITER = 0
    ROUND = 1
    BEVEL = 2

class PDFStyleKeys(Enum):
    """An enumeration of the graphics state parameter dictionary keys."""
    FILL_ALPHA = Name("ca")
    BLEND_MODE = Name("BM")
    STROKE_ALPHA = Name("CA")
    STROKE_ADJUSTMENT = Name("SA")
    STROKE_WIDTH = Name("LW")
    STROKE_CAP_STYLE = Name("LC")
    STROKE_JOIN_STYLE = Name("LJ")
    STROKE_MITER_LIMIT = Name("ML")
    STROKE_DASH_PATTERN = Name("D")

class Corner(CoerciveEnum):
    """An enumeration."""
    TOP_RIGHT = "TOP_RIGHT"
    TOP_LEFT = "TOP_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"

class FontDescriptorFlags(Flag):
    """
    An enumeration of the flags for the unsigned 32-bit integer entry in the font descriptor specifying various
    characteristics of the font. Bit positions are numbered from 1 (low-order) to 32 (high-order).
    """
    FIXED_PITCH = 1
    SYMBOLIC = 4
    ITALIC = 64
    FORCE_BOLD = 262144

class AccessPermission(IntFlag):
    """Permission flags will translate as an integer on the encryption dictionary"""
    PRINT_LOW_RES = 4
    MODIFY = 8
    COPY = 16
    ANNOTATION = 32
    FILL_FORMS = 256
    COPY_FOR_ACCESSIBILITY = 512
    ASSEMBLE = 1024
    PRINT_HIGH_RES = 2048
    @classmethod
    def all(cls) -> int:
        """All flags enabled"""
        ...
    @classmethod
    def none(cls) -> Literal[0]:
        """All flags disabled"""
        ...

class EncryptionMethod(Enum):
    """Algorithm to be used to encrypt the document"""
    NO_ENCRYPTION = 0
    RC4 = 1
    AES_128 = 2
    AES_256 = 3

class TextDirection(CoerciveEnum):
    """Text rendering direction for text shaping"""
    LTR = "LTR"
    RTL = "RTL"
    TTB = "TTB"
    BTT = "BTT"

class OutputIntentSubType(CoerciveEnum):
    """Definition for Output Intent Subtypes"""
    PDFX = "GTS_PDFX"
    PDFA = "GTS_PDFA1"
    ISOPDF = "ISO_PDFE1"

class PageLabelStyle(CoerciveEnum):
    """Style of the page label"""
    NUMBER = "D"
    UPPER_ROMAN = "R"
    LOWER_ROMAN = "r"
    UPPER_LETTER = "A"
    LOWER_LETTER = "a"
    NONE = None

class Duplex(CoerciveEnum):
    """The paper handling option that shall be used when printing the file from the print dialog."""
    SIMPLEX = "Simplex"
    DUPLEX_FLIP_SHORT_EDGE = "DuplexFlipShortEdge"
    DUPLEX_FLIP_LONG_EDGE = "DuplexFlipLongEdge"

class PageBoundaries(CoerciveEnum):
    """An enumeration."""
    ART_BOX = "ArtBox"
    BLEED_BOX = "BleedBox"
    CROP_BOX = "CropBox"
    MEDIA_BOX = "MediaBox"
    TRIM_BOX = "TrimBox"

class PageOrientation(CoerciveEnum):
    """An enumeration."""
    PORTRAIT = "P"
    LANDSCAPE = "L"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class PDFResourceType(Enum):
    """An enumeration."""
    EXT_G_STATE = "ExtGState"
    COLOR_SPACE = "ColorSpace"
    PATTERN = "Pattern"
    SHADDING = "Shading"
    X_OBJECT = "XObject"
    FONT = "Font"
    PROC_SET = "ProcSet"
    PROPERTIES = "Properties"
