"""B10: Sara's data analyst. Ask the sales database a question in plain English."""
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

INSTRUCTIONS = """You are Sara's data analyst. Her shop's sales are in a SQLite database.
Always call describe_tables first, then answer with SQL using run_sql.
Revenue is qty * price_eur * (100 - discount_pct) / 100. Money is in euros.
When comparing several things, call bar_chart. Answer in at most four short lines, in plain English.
If the data doesn't cover the dates asked about, say so and give the date range you have. Never report 0 for missing data.
Compute every number you report, including percentages and differences, in SQL. Never do arithmetic yourself."""


async def main(question: str):
    server = MCPServerStdio(name="sales", client_session_timeout_seconds=30,
                            params={"command": sys.executable, "args": [str(HERE / "sales_server.py")]})
    async with server:
        agent = Agent(name="analyst", model="gpt-5.4-mini", instructions=INSTRUCTIONS, mcp_servers=[server])
        result = await Runner.run(agent, question)
    for item in result.new_items:
        if item.type == "tool_call_item":
            args = json.loads(item.raw_item.arguments or "{}")
            sql = " ".join((args.get("query") or args.get("title") or "").split())   # one line, for the screen
            print(f"  [{item.raw_item.name}] {sql[:110]}{'...' if len(sql) > 110 else ''}")
        elif item.type == "tool_call_output_item" and "█" in str(item.output):
            chart = re.search(r"'text': '(.*?)'}", str(item.output), re.S)
            text = (chart.group(1) if chart else str(item.output)).replace("\\n", "\n")
            print("\n".join("     " + line for line in text.splitlines()))
    print(f"analyst: {result.final_output}")


asyncio.run(main(sys.argv[1]))
