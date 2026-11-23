"""B11: Sara's company knowledge agent. Answers only from her documents, with sources, or says it doesn't know."""
import asyncio
import json
import re
import sys
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv(override=True)
HERE = Path(__file__).parent

INSTRUCTIONS = """You answer questions from Sara's team using only her company documents.
Always call search_docs first. Answer only from what the search returns.
After every fact, cite its source like [staff_guide.md § Holidays].
If the documents don't answer the question, say exactly: "I don't know, the documents don't cover that. Please ask Sara."
Never guess. At most three sentences."""


async def main(question: str):
    server = MCPServerStdio(name="knowledge", client_session_timeout_seconds=30,
                            params={"command": sys.executable, "args": [str(HERE / "kb_server.py")]})
    async with server:
        agent = Agent(name="knowledge", model="gpt-5.4-mini", instructions=INSTRUCTIONS, mcp_servers=[server])
        result = await Runner.run(agent, question)
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"  [search_docs] {json.loads(item.raw_item.arguments)['query']}")
        elif item.type == "tool_call_output_item":
            for source, score in re.findall(r"\[(.+?)\] \(score ([\d.]+)\)", str(item.output)):
                print(f"     {score}  {source}")
    print(f"answer: {result.final_output}")


asyncio.run(main(sys.argv[1]))
