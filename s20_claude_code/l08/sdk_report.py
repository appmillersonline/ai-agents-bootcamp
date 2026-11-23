"""The same weekly-report skill from lecture 3, now used from our own Python app through the Agent SDK."""
from pathlib import Path

import anyio
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock, query

SHOP = Path(__file__).parents[1] / "l03" / "with_skill"     # the folder with .claude/skills/weekly-report

options = ClaudeAgentOptions(
    cwd=str(SHOP),
    setting_sources=["project"],                 # load the project's skills
    allowed_tools=["Skill", "Read", "Write", "Bash(python .claude/skills/weekly-report/summary.py:*)"],
    max_turns=8,
)


async def main():
    async for message in query(prompt="How did the shop do this week? Write the report.", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"  [tool] {block.name} {block.input.get('skill') or block.input.get('command') or ''}")
        elif isinstance(message, ResultMessage):
            print(f"  result: {message.result}")
            print(f"== {message.num_turns} turns, ${message.total_cost_usd:.3f}")


anyio.run(main)
