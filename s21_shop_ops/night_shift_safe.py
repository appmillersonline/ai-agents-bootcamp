"""Project 9, version 2: the same night shift, but sending an email needs Sara's approval. Enforced in code."""
import sys
from dataclasses import replace

import anyio
from claude_agent_sdk import (AssistantMessage, PermissionResultAllow, PermissionResultDeny, ResultMessage,
                              ToolUseBlock, query)

from night_shift import options

AUDIT = "audit.log"


async def guard(tool_name, tool_input, context):
    """Called by the SDK before any tool that isn't pre-approved. We decide, not the model."""
    with open(AUDIT, "a") as log:
        log.write(f"{tool_name} {tool_input.get('to', '')}\n")
    if tool_name == "mcp__shop__send_email":
        return PermissionResultDeny(message="Sending needs Sara's approval. Save it with draft_email instead.")
    return PermissionResultAllow()


safe = replace(options,
               allowed_tools=[t for t in options.allowed_tools if t != "mcp__shop__send_email"],  # no longer pre-approved
               can_use_tool=guard)


async def as_stream(text):                       # can_use_tool needs the prompt as a stream of messages
    yield {"type": "user", "message": {"role": "user", "content": text}}


async def main():
    task = sys.argv[1] if len(sys.argv) > 1 else "Start the night shift."
    async for message in query(prompt=as_stream(task), options=safe):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"  [{block.name.removeprefix('mcp__shop__')}] {block.input.get('to', '')}")
        elif isinstance(message, ResultMessage):
            print(f"== done: {message.num_turns} turns, ${message.total_cost_usd:.3f}")


anyio.run(main)
