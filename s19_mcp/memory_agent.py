"""Long-term memory through MCP: Anthropic's memory server keeps a small knowledge graph in a file."""
import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv(override=True)
MEMORY_FILE = str(Path(__file__).parent / "memory" / "sara_memory.jsonl")
MEMORY = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"],
          "env": {"MEMORY_FILE_PATH": MEMORY_FILE}}
INSTRUCTIONS = ("You are Sara's shop assistant. Use your memory tools to store facts about customers "
                "and to look them up before you answer. The search matches exact words, so search with "
                "just the customer's name, like 'Hotel Linden'. Be brief.")


async def main():
    message = sys.argv[1]
    async with MCPServerStdio(params=MEMORY, name="memory", client_session_timeout_seconds=60) as memory:
        agent = Agent(name="shop_assistant", instructions=INSTRUCTIONS, model="gpt-5.4-mini", mcp_servers=[memory])
        result = await Runner.run(agent, message)
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"   [tool] {item.raw_item.name}({item.raw_item.arguments})")
    print(f"Sara: {message}")
    print(f"assistant: {result.final_output}")


asyncio.run(main())
