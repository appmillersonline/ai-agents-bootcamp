"""The swap test. Same resume, different name and birth year: the score must not change."""
import asyncio

from agents import Runner

from hiring_kit import DATA, fairness_problems, load, points, scorer


async def main():
    for path in sorted((DATA / "hiring" / "swap_test").glob("*.txt")):
        details, history = load(path)
        result = await Runner.run(scorer, history)
        a = result.final_output
        problems = fairness_problems(a) or "none"
        print(f"{details['Name']:<14} born {details['Date of birth'][-4:]}  {points(a)} points  "
              f"agent saw {len(history)} characters, no name  fairness problems: {problems}")


asyncio.run(main())
