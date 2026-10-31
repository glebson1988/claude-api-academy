from pathlib import Path
from urllib.parse import unquote, urlsplit

from mcp.server.fastmcp import Context
from mcp.shared.exceptions import McpError


def file_url_to_path(uri: object) -> Path:
    url = urlsplit(str(uri))
    if url.scheme != "file" or url.netloc not in ("", "localhost"):
        raise ValueError(f"Only local file URIs are supported: {uri}")
    return Path(unquote(url.path)).resolve()


async def get_root_paths(ctx: Context) -> list[Path]:
    try:
        result = await ctx.session.list_roots()
    except McpError as exc:
        raise ValueError("Could not obtain roots from the client") from exc
    return [file_url_to_path(root.uri) for root in result.roots]


async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    path = requested_path.expanduser().resolve()
    roots = await get_root_paths(ctx)
    return any(root.is_dir() and path.is_relative_to(root) for root in roots)


async def require_allowed_path(path: str, ctx: Context) -> Path:
    requested = Path(path).expanduser()
    if not requested.is_absolute():
        raise ValueError("Use an absolute path; call list_roots to find available roots")
    requested = requested.resolve()
    if not await is_path_allowed(requested, ctx):
        raise ValueError(f"Access to path is not allowed: {path}")
    if not requested.exists():
        raise ValueError(f"Path does not exist: {path}")
    return requested
