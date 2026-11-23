"""Score every resume at once, and rank them. The table shows candidate numbers, not names."""
import asyncio

from agents import Runner, trace

from hiring_kit import MUST_HAVES, RESUMES, Assessment, load, met, points, scorer


async def assess(path) -> tuple[str, Assessment]:
    details, history = load(path)
    result = await Runner.run(scorer, history)
    return path.stem, result.final_output


async def assess_all() -> list[tuple[str, Assessment]]:
    with trace("Rank resumes"):
        results = await asyncio.gather(*(assess(p) for p in RESUMES))
    return sorted(results, key=lambda r: points(r[1]), reverse=True)


if __name__ == "__main__":
    for candidate, a in asyncio.run(assess_all()):
        musts = len(met(a) & MUST_HAVES)
        flag = "shortlist" if musts == len(MUST_HAVES) else ""
        print(f"{candidate}  {points(a):>3} points  must-haves {musts}/4  {flag}")
