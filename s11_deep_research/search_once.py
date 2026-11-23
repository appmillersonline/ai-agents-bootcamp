"""Try the search agent on its own, with one search term."""
import asyncio

from agents import Runner, trace

from search_agent import search_agent


async def main():
    with trace("One search"):
        result = await Runner.run(search_agent, "wholesale candle prices for cafes 2026")
    print(result.final_output)


asyncio.run(main())
