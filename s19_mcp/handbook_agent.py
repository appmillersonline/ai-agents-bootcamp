"""Sara's shop helper (OpenAI Agents SDK) answers from the handbook, using tools from an MCP server."""
import asyncio
from pathlib import Path

from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio, create_static_tool_filter
from dotenv import load_dotenv

load_dotenv(override=True)
DATA = str(Path(__file__).parents[1] / "data")


async def main():
    params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", DATA]}
    read_only = create_static_tool_filter(allowed_tool_names=["list_directory", "read_text_file"])
    async with MCPServerStdio(params=params, name="files", tool_filter=read_only, client_session_timeout_seconds=30) as files:
        agent = Agent(
            name="shop_helper",
            instructions=f"You answer customers of Sara's shop. The shop's files are in {DATA}. "
                         "Find the answer in shop_handbook.md and reply in two short sentences.",
            model="gpt-5.4-mini",
            mcp_servers=[files],
        )
        with trace("handbook via MCP"):
            result = await Runner.run(agent, "Can I return a candle I already lit once?")
        for item in result.new_items:
            if item.type == "tool_call_item":
                print(f"   [tool] {item.raw_item.name}")
        print(f"shop_helper: {result.final_output}")


asyncio.run(main())
