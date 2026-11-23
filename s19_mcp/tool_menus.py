"""Read the menus of three ready-made MCP servers: Fetch, Playwright (browser) and Files."""
import asyncio
from pathlib import Path

from agents.mcp import MCPServerStdio

DATA = str(Path(__file__).parents[1] / "data")
FETCH = {"command": "uvx", "args": ["mcp-server-fetch"]}
BROWSER = {"command": "npx", "args": ["-y", "@playwright/mcp@latest", "--headless", "--isolated"]}
FILES = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", DATA]}


async def menu(name: str, params: dict) -> list:
    async with MCPServerStdio(params=params, name=name, client_session_timeout_seconds=60) as server:
        return await server.list_tools()


async def main():
    fetch = await menu("fetch", FETCH)
    print("FETCH description, as written by Anthropic:")
    print("  " + fetch[0].description.replace("\n", " ")[:330])
    print("  inputs:", ", ".join(fetch[0].inputSchema["properties"]))
    browser = await menu("browser", BROWSER)
    print(f"\nPLAYWRIGHT (Microsoft): {len(browser)} tools")
    print("  " + ", ".join(t.name for t in browser[:12]) + ", ...")
    files = await menu("files", FILES)
    print(f"\nFILES (Anthropic): {len(files)} tools")


asyncio.run(main())
