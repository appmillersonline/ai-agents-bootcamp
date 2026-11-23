"""The same job two ways: a plain function vs. an MCP server. Same answer, very different cost."""
import asyncio
import time
from pathlib import Path

from agents.mcp import MCPServerStdio

DATA = Path(__file__).parents[1] / "data"


def read_stock() -> str:
    """A plain Python tool: read Sara's stock list."""
    return (DATA / "inventory.csv").read_text()


async def main():
    start = time.perf_counter()
    plain = read_stock()
    plain_ms = (time.perf_counter() - start) * 1000

    params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", str(DATA)]}
    start = time.perf_counter()
    async with MCPServerStdio(params=params, name="files", client_session_timeout_seconds=60) as files:
        ready_ms = (time.perf_counter() - start) * 1000
        start = time.perf_counter()
        result = await files.call_tool("read_text_file", {"path": str(DATA / "inventory.csv")})
        call_ms = (time.perf_counter() - start) * 1000
    via_mcp = result.content[0].text

    print(f"plain function : {plain_ms:8.2f} ms")
    print(f"MCP server     : {ready_ms:8.2f} ms to start + {call_ms:.2f} ms per call")
    print(f"same answer?   : {plain == via_mcp}")
    print(f"extra moving parts with MCP: a second process (Node), a handshake, JSON messages")


asyncio.run(main())
