"""Project 9, version 1: the nightly Shop Ops Agent. Checks stock and late orders, writes emails and a report."""
import sys

import anyio
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, ToolUseBlock, query

from shop_tools import shop

ROUTINE = """You are the night shift for Sara's small online shop. Today is 7 November 2026.
1. Check low stock. For each low product, email its supplier a reorder: enough full packs to get back above twice the reorder level.
2. Check late orders. Email each customer a short, warm update and an apology.
3. Save a morning report for Sara: what you found and every email, in under 150 words.
Use the shop tools only. Be brief."""

options = ClaudeAgentOptions(
    system_prompt=ROUTINE,
    mcp_servers={"shop": shop},
    allowed_tools=["mcp__shop__low_stock", "mcp__shop__late_orders", "mcp__shop__send_email",
                   "mcp__shop__draft_email", "mcp__shop__save_report"],
    max_turns=20,
    max_budget_usd=1.00,
    setting_sources=[],
)


async def main():
    task = sys.argv[1] if len(sys.argv) > 1 else "Start the night shift."
    async for message in query(prompt=task, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    detail = block.input.get("to", "")
                    print(f"  [{block.name.removeprefix('mcp__shop__')}] {detail}")
        elif isinstance(message, ResultMessage):
            print(f"== done: {message.num_turns} turns, ${message.total_cost_usd:.3f}")


if __name__ == "__main__":
    anyio.run(main)
