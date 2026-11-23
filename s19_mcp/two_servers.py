"""One agent, two ready-made MCP servers: Files reads Sara's brief, Fetch reads the web."""
import asyncio
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, create_static_tool_filter
from dotenv import load_dotenv

load_dotenv(override=True)
DATA = str(Path(__file__).parents[1] / "data")
FILES = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", DATA]}
FETCH = {"command": "uvx", "args": ["mcp-server-fetch"]}

TASK = (f"Read {DATA}/launch_brief.md. Then fetch https://en.wikipedia.org/wiki/Lavandula and find one true, "
        "interesting fact about lavender. Write a product blurb of at most 60 words for the gift box that uses "
        "the brief's facts plus that one lavender fact. End with: Source: <the page you used>.")


async def main():
    read_only = create_static_tool_filter(allowed_tool_names=["read_text_file"])
    async with MCPServerStdio(params=FILES, name="files", tool_filter=read_only, client_session_timeout_seconds=60) as files, \
               MCPServerStdio(params=FETCH, name="fetch", client_session_timeout_seconds=60) as fetch:
        agent = Agent(name="copywriter", model="gpt-5.4-mini", mcp_servers=[files, fetch],
                      instructions="You write short, warm product copy for Sara's shop. Use only facts you have read.")
        result = await Runner.run(agent, TASK)
        for item in result.new_items:
            if item.type == "tool_call_item":
                print(f"   [tool] {item.raw_item.name}")
        print(result.final_output)


asyncio.run(main())
