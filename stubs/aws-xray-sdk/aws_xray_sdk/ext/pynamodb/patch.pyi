from typing import Final

PYNAMODB4: Final[bool]

def patch() -> None:
    """Patch PynamoDB so it generates subsegements when calling DynamoDB."""
    ...
def pynamodb_meta_processor(wrapped, instance, args, kwargs, return_value, exception, subsegment, stack) -> None: ...
