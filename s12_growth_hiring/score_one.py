"""Check one resume against the job, requirement by requirement."""
import asyncio

from agents import Runner

from hiring_kit import RESUMES, load, points, scorer


async def main():
    details, history = load(RESUMES[4])
    result = await Runner.run(scorer, history)
    a = result.final_output
    for c in a.checks:
        print(f"{'YES' if c.met else 'no '}  {c.requirement}. {c.evidence}")
    print(f"\n{points(a)} points. {a.summary}")


asyncio.run(main())
