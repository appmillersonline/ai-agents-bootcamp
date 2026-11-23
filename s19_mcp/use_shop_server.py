"""Use Sara's own MCP server: list its tools, then let an agent answer a customer with it."""
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv(override=True)
SERVER = {"command": sys.executable, "args": [str(Path(__file__).parent / "shop_server.py")]}


async def main():
    async with MCPServerStdio(params=SERVER, name="sara-shop", client_session_timeout_seconds=30) as shop:
        for t in await shop.list_tools():
            print(f"- {t.name}: {t.description.splitlines()[0]}")
        agent = Agent(name="shop_helper", model="gpt-5.4-mini", mcp_servers=[shop],
                      instructions="You answer customers of Sara's shop in two short sentences. Use the shop's tools.")
        result = await Runner.run(agent, "Hi, it's Maya. Has my order 1042 shipped? And is the candle trio back in stock?")
    print()
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"   [tool] {item.raw_item.name}({item.raw_item.arguments})")
    print("shop_helper:", result.final_output)


asyncio.run(main())
