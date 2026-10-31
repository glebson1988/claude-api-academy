import asyncio
import sys
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.claude import Claude
from core.sampling import create_sampling_callback

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)


async def main():
    claude_service = Claude(model=claude_model)
    sampling_callback = create_sampling_callback(claude_service)

    parser = argparse.ArgumentParser(description="MCP Chat")
    parser.add_argument("server_scripts", nargs="*", help="Additional MCP server scripts")
    parser.add_argument(
        "--root", action="append", default=[], metavar="DIRECTORY",
        help="Allow filesystem access inside this directory (repeatable)",
    )
    options = parser.parse_args()
    for root in options.root:
        if not Path(root).expanduser().is_dir():
            parser.error(f"Root must be an existing directory: {root}")
    server_scripts = options.server_scripts
    clients = {}

    command = sys.executable
    args = [str(Path(__file__).with_name("mcp_server.py"))]

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(
                command=command, args=args, sampling_callback=sampling_callback,
                roots=options.root,
            )
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(
                    command=sys.executable, args=[str(Path(server_script).resolve())],
                    sampling_callback=sampling_callback,
                    roots=options.root,
                )
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
