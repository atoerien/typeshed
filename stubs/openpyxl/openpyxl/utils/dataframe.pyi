from _typeshed import Incomplete
from collections.abc import Generator

def dataframe_to_rows(df, index: bool = True, header: bool = True) -> Generator[Incomplete]:
    """
    Convert a Pandas dataframe into something suitable for passing into a worksheet.
    If index is True then the index will be included, starting one row below the header.
    If header is True then column headers will be included starting one column to the right.
    Formatting should be done by client code.
    """
    ...
def expand_index(index, header: bool = False) -> Generator[Incomplete]:
    """
    Expand axis or column Multiindex
    For columns use header = True
    For axes use header = False (default)
    """
    ...
