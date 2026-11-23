"""Print what FastMCP built from our docstrings and type hints: exactly what a model is shown."""
import asyncio
import json
import sys
from pathlib import Path

from agents.mcp import MCPServerStdio

SERVER = {"command": sys.executable, "args": [str(Path(__file__).parent / "shop_server.py")]}


async def main():
    async with MCPServerStdio(params=SERVER, name="sara-shop", client_session_timeout_seconds=30) as shop:
        tool = next(t for t in await shop.list_tools() if t.name == "check_stock")
        print("name:", tool.name)
        print("description:", tool.description)
        print("inputSchema:", json.dumps(tool.inputSchema, indent=2))


asyncio.run(main())
