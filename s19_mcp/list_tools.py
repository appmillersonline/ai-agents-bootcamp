"""Start an MCP server and ask it which tools it offers. No model, no agent: just the protocol."""
import asyncio
from pathlib import Path

from agents.mcp import MCPServerStdio

DATA = str(Path(__file__).parents[1] / "data")


async def main():
    params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", DATA]}
    async with MCPServerStdio(params=params, name="files", client_session_timeout_seconds=30) as server:
        tools = await server.list_tools()
        print(f"The 'files' server offers {len(tools)} tools:")
        for t in tools:
            print(f"  - {t.name}: {t.description.splitlines()[0][:70]}")


asyncio.run(main())
