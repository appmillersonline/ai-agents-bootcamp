"""Same question, two ways of serving the same API: 20 flat tools vs. 2 'explore' tools. Measure it."""
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, create_static_tool_filter
from dotenv import load_dotenv

load_dotenv(override=True)
API = str(Path(__file__).parent / "shop_api.py")
QUESTION = "Jess Brown says her order 1044 is late. What's its status, and what does our damage policy say if it arrives broken?"


SUPPORT_TOOLS = ["get_order", "get_stock", "returns_policy", "damage_policy"]   # what a support agent needs


async def ask(mode: str, args: list[str], tool_filter=None) -> None:
    params = {"command": sys.executable, "args": [API, *args]}
    async with MCPServerStdio(params=params, name="shop-api", tool_filter=tool_filter, client_session_timeout_seconds=30) as api:
        tools = await api.list_tools()
        agent = Agent(name="support", model="gpt-5.4-mini", mcp_servers=[api],
                      instructions="You help Sara's shop answer customers. Use the shop API. Be brief.")
        result = await Runner.run(agent, QUESTION)
    usage = result.context_wrapper.usage
    calls = [i.raw_item.name for i in result.new_items if i.type == "tool_call_item"]
    print(f"== {mode}: {len(tools)} tools shown")
    print(f"   tool calls  : {' -> '.join(calls)}")
    print(f"   input tokens: {usage.input_tokens}  (over {usage.requests} model calls)")
    print(f"   answer      : {result.final_output}\n")


async def main():
    await ask("all 20 tools", [])
    await ask("filtered", [], create_static_tool_filter(allowed_tool_names=SUPPORT_TOOLS))
    await ask("progressive", ["--progressive"])


asyncio.run(main())
