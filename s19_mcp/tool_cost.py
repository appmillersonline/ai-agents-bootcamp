"""What does a tool list cost? The same one-line question with 0, 20 and ~60 tools attached."""
import asyncio
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv(override=True)
HERE = Path(__file__).parent
SERVERS = {
    "shop api": {"command": sys.executable, "args": [str(HERE / "shop_api.py")]},
    "files": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", str(HERE.parent / "data")]},
    "browser": {"command": "npx", "args": ["-y", "@playwright/mcp@latest", "--headless", "--isolated"]},
    "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]},
}


async def cost(names: list[str]) -> None:
    async with AsyncExitStack() as stack:
        servers = [await stack.enter_async_context(MCPServerStdio(params=SERVERS[n], name=n, client_session_timeout_seconds=60))
                   for n in names]
        n_tools = 0
        for server in servers:
            n_tools += len(await server.list_tools())
        agent = Agent(name="support", model="gpt-5.4-mini", mcp_servers=servers, instructions="Be brief.")
        result = await Runner.run(agent, "Say hello to Sara in five words.")
    print(f"{n_tools:3d} tools ({', '.join(names) or 'none'}): {result.context_wrapper.usage.input_tokens:5d} input tokens")


async def main():
    await cost([])
    await cost(["shop api"])
    await cost(["shop api", "files", "browser", "fetch"])


asyncio.run(main())
