"""Spot what changed for one competitor this week."""
import asyncio

from agents import Runner

from competitors import page, spotter


async def main():
    name = "Wick & Co"
    prompt = f"Competitor: {name}\n\nLAST WEEK:\n{page(name, 'last_week')}\n\nTHIS WEEK:\n{page(name, 'this_week')}"
    result = await Runner.run(spotter, prompt)
    for change in result.final_output.changes:
        print(f"[{change.kind}] {change.item}: {change.before} -> {change.after}")
        print(f"   Why it matters: {change.why_it_matters}")


asyncio.run(main())
