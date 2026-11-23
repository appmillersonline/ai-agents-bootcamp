"""Start the server once, then make fifty calls: the start-up cost spreads out."""
import asyncio
import time
from pathlib import Path

from agents.mcp import MCPServerStdio

DATA = Path(__file__).parents[1] / "data"


async def main():
    params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", str(DATA)]}
    start = time.perf_counter()
    async with MCPServerStdio(params=params, name="files", client_session_timeout_seconds=60) as files:
        ready = time.perf_counter() - start
        calls = time.perf_counter()
        for _ in range(50):
            await files.call_tool("read_text_file", {"path": str(DATA / "inventory.csv")})
        calls = time.perf_counter() - calls
    total = ready + calls
    print(f"start once : {ready * 1000:7.0f} ms")
    print(f"50 calls   : {calls * 1000:7.0f} ms  ({calls * 1000 / 50:.1f} ms each)")
    print(f"average per call, start included: {total * 1000 / 50:.1f} ms")


asyncio.run(main())
