"""See the planner's plan. Notice each reason comes before its search."""
import asyncio

from agents import Runner

from planner_agent import planner_agent

QUESTION = "What do cafés and boutique hotels pay for candles, and what do they look for in a supplier?"


async def main():
    result = await Runner.run(planner_agent, QUESTION)
    for i, item in enumerate(result.final_output.searches, 1):
        print(f"{i}. Why: {item.reason}\n   Search: {item.query}\n")


asyncio.run(main())
