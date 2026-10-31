from mcp import types


async def logging_callback(params: types.LoggingMessageNotificationParams):
    print(f"[MCP {params.level}] {params.data}", flush=True)


async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None and total > 0:
        status = f"{progress:g}/{total:g} ({progress / total * 100:.0f}%)"
    elif total is not None:
        status = f"{progress:g}/{total:g}"
    else:
        status = f"{progress:g}"
    suffix = f" — {message}" if message else ""
    print(f"[Progress] {status}{suffix}", flush=True)
