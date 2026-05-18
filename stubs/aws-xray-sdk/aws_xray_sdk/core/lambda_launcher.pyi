from logging import Logger
from typing import Final

from .context import Context

log: Logger
LAMBDA_TRACE_HEADER_KEY: Final = "_X_AMZN_TRACE_ID"
LAMBDA_TASK_ROOT_KEY: Final = "LAMBDA_TASK_ROOT"
TOUCH_FILE_DIR: Final = "/tmp/.aws-xray/"
TOUCH_FILE_PATH: Final = "/tmp/.aws-xray/initialized"

def check_in_lambda() -> LambdaContext | None:
    """
    Return None if SDK is not loaded in AWS Lambda worker.
    Otherwise drop a touch file and return a lambda context.
    """
    ...

class LambdaContext(Context):
    """
    Lambda service will generate a segment for each function invocation which
    cannot be mutated. The context doesn't keep any manually created segment
    but instead every time ``get_trace_entity()`` gets called it refresh the
    segment based on environment variables set by Lambda worker.
    """
    def __init__(self) -> None: ...

    @property  # type: ignore[override]
    def context_missing(self) -> None: ...
    @context_missing.setter
    def context_missing(self, value: str) -> None: ...
