"""Ask Sara's handbook by meaning: the agent can only search (qdrant-find), never write."""
import asyncio
import json

from agents import Agent, Runner
from agents.mcp import create_static_tool_filter, MCPServerStdio
from dotenv import load_dotenv

from rag_store import QDRANT

load_dotenv(override=True)
QUESTIONS = ["My mug arrived in pieces. What can you do?",
             "Can I put the vase in my dishwasher?"]


async def main():
    find_only = create_static_tool_filter(allowed_tool_names=["qdrant-find"])
    async with MCPServerStdio(params=QDRANT, name="handbook", tool_filter=find_only, client_session_timeout_seconds=120) as handbook:
        agent = Agent(name="support", model="gpt-5.4-mini", mcp_servers=[handbook],
                      instructions="You answer Sara's customers. Always call qdrant-find first, then answer using only the "
                                   "rules it returns. If nothing fits, say you'll ask Sara. Two short sentences.")
        for question in QUESTIONS:
            result = await Runner.run(agent, question)
            searches = [json.loads(i.raw_item.arguments)["query"] for i in result.new_items if i.type == "tool_call_item"]
            print(f"Customer: {question}")
            print(f"   [qdrant-find] {searches}")
            print(f"support: {result.final_output}\n")


asyncio.run(main())
