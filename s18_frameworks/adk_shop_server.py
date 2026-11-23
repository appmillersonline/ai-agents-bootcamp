"""Sara's own MCP server, used from a different framework (Google ADK) without changing a line of it."""
import asyncio
import logging
from pathlib import Path

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

from shop_helper.agent import MODEL

logging.getLogger("google_adk").setLevel(logging.ERROR)
ROOT = Path(__file__).parents[1]

shop = McpToolset(connection_params=StdioConnectionParams(
    server_params=StdioServerParameters(command=str(ROOT / ".venv/bin/python"), args=[str(ROOT / "s19_mcp/shop_server.py")]),
    timeout=30))
agent = Agent(name="adk_shop_helper", model=MODEL, tools=[shop],
              instruction="You help Sara run her shop. Use the shop's tools. Be brief.")


async def main():
    runner = InMemoryRunner(agent=agent, app_name="shop")
    events = await runner.run_debug("Which products need reordering?", quiet=True)
    for e in events:
        for call in e.get_function_calls():
            print(f"   [{e.author}] calls {call.name}")
    print("adk_shop_helper:", events[-1].content.parts[0].text)
    await shop.close()


asyncio.run(main())
