"""A remote MCP server in an agent: Context7 looks up current library docs over streamable HTTP."""
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from dotenv import load_dotenv

load_dotenv(override=True)
QUESTION = ("In the OpenAI Agents SDK for Python, what does create_static_tool_filter do, "
            "and what are its two arguments? Answer in two sentences, from the docs.")


async def main():
    async with MCPServerStreamableHttp(params={"url": "https://mcp.context7.com/mcp"}, name="context7",
                                       client_session_timeout_seconds=60) as context7:
        agent = Agent(name="docs_helper", model="gpt-5.4-mini", mcp_servers=[context7],
                      instructions="Answer coding questions using Context7 docs. Don't guess.")
        result = await Runner.run(agent, QUESTION)
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"   [tool] {item.raw_item.name}")
    print(result.final_output)


asyncio.run(main())
