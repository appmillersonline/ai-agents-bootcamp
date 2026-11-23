"""Sara's shop helper on the Claude Agent SDK: Claude Code's engine, with our own tool, inside our own script."""
import csv
from pathlib import Path

import anyio
from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, ToolUseBlock,
                              create_sdk_mcp_server, query, tool)

INVENTORY = Path(__file__).parents[2] / "data" / "inventory.csv"


@tool("low_stock", "List the products at or below their reorder level, with how many are in stock.", {})
async def low_stock(args):
    rows = [r for r in csv.DictReader(open(INVENTORY)) if int(r["in_stock"]) <= int(r["reorder_at"])]
    text = "\n".join(f"{r['item']}: {r['in_stock']} in stock (reorder at {r['reorder_at']})" for r in rows)
    return {"content": [{"type": "text", "text": text or "Nothing is low."}]}


shop = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[low_stock])   # an MCP server in our own process

options = ClaudeAgentOptions(
    system_prompt="You are Sara's shop helper. Use the shop tools. Answer in three short lines.",
    mcp_servers={"shop": shop},
    allowed_tools=["mcp__shop__low_stock"],     # nothing else: no files, no shell
    max_turns=5,
    max_budget_usd=0.50,                         # a hard spending limit for this run
    setting_sources=[],                          # ignore any CLAUDE.md or settings on this machine
)


async def main():
    async for message in query(prompt="What's running low, and how many of each should we order to get back to 20?", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"  [tool] {block.name}")
                elif isinstance(block, TextBlock):
                    print(f"  helper: {block.text}")
        elif isinstance(message, ResultMessage):
            print(f"== {message.num_turns} turns, ${message.total_cost_usd:.3f}")


if __name__ == "__main__":
    anyio.run(main)
