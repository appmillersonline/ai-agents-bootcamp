"""Three kinds of MCP server: local, local-calling-the-web, and remote. Same question for each."""
import asyncio
from pathlib import Path

from agents.mcp import MCPServerStdio, MCPServerStreamableHttp

DATA = str(Path(__file__).parents[1] / "data")
SERVERS = [
    ("files    (local, works on your disk)", MCPServerStdio,
     {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", DATA]}),
    ("fetch    (local, calls the web)", MCPServerStdio,
     {"command": "uvx", "args": ["mcp-server-fetch"]}),
    ("context7 (remote, over HTTP)", MCPServerStreamableHttp,
     {"url": "https://mcp.context7.com/mcp"}),
]


async def main():
    for label, kind, params in SERVERS:
        async with kind(params=params, name=label, client_session_timeout_seconds=30) as server:
            tools = await server.list_tools()
            names = ", ".join(t.name for t in tools[:3])
            print(f"{label}: {len(tools)} tools -> {names}{' ...' if len(tools) > 3 else ''}")


asyncio.run(main())
