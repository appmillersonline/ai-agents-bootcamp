"""The same helper with a one-cent budget: the SDK stops the run when the limit is reached."""
from dataclasses import replace

import anyio
from claude_agent_sdk import ResultError, ResultMessage, query

from sdk_helper import options

tiny = replace(options, max_budget_usd=0.01)


async def main():
    try:
        async for message in query(prompt="What's running low, and how many of each should we order?", options=tiny):
            if isinstance(message, ResultMessage):
                print(f"finished: ${message.total_cost_usd:.3f}")
    except ResultError as e:                       # the SDK raises when the run ends in an error
        print(f"stopped by the SDK: {e}")


anyio.run(main)
