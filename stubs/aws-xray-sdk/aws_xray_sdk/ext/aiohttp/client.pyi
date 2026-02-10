"""AioHttp Client tracing, only compatible with Aiohttp 3.X versions"""

from typing import Final

REMOTE_NAMESPACE: Final = "remote"
LOCAL_NAMESPACE: Final = "local"
LOCAL_EXCEPTIONS: tuple[type[Exception], ...]

async def begin_subsegment(session, trace_config_ctx, params): ...
async def end_subsegment(session, trace_config_ctx, params): ...
async def end_subsegment_with_exception(session, trace_config_ctx, params): ...
def aws_xray_trace_config(name=None):
    """
    :param name: name used to identify the subsegment, with None internally the URL will
                 be used as identifier.
    :returns: TraceConfig.
    """
    ...
