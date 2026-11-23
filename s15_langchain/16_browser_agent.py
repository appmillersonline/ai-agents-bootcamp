import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

import shop  # noqa: F401

BROWSER = {
    "playwright": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@playwright/mcp@0.0.84", "--headless", "--isolated"],
    }
}

TASK = (
    "Go to http://localhost:8015, the website of Wick & Co, a competitor of Sara's Shop. "
    "Find their candle prices and any sale. Then compare with Sara's prices: "
    "Lavender candle 12 euros, Candle trio 22 euros."
)


@wrap_tool_call
async def log_tool_calls(request, handler):
    call = request.tool_call
    print(f"  [browser] {call['name']} {call['args']}")
    return await handler(request)


async def main():
    client = MultiServerMCPClient(BROWSER)
    async with client.session("playwright") as session:  # one browser for the whole task
        await run(session)


async def run(session):
    tools = await load_mcp_tools(session)
    print(f"The Playwright MCP server gave us {len(tools)} tools:")
    print("  " + ", ".join(t.name for t in tools) + "\n")

    agent = create_agent(
        model="openai:gpt-5.4-mini",
        tools=tools,
        system_prompt="You research competitor websites with the browser tools. Read pages with browser_snapshot; avoid screenshots.",
        middleware=[log_tool_calls],
    )
    result = await agent.ainvoke({"messages": [("user", TASK)]})
    print("\n" + result["messages"][-1].content)


asyncio.run(main())
