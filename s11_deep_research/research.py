"""Run the whole research team from the terminal."""
import asyncio

from research_manager import run

QUESTION = "What do cafés and boutique hotels pay for candles, and what do they look for in a supplier?"


async def main():
    async for update in run(QUESTION):
        if isinstance(update, str):
            print(update)
        else:
            print("\nSummary:", update.summary)


asyncio.run(main())
