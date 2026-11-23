"""Runs the four agents in order, with plain code. Yields a status line after each step."""
import asyncio
import time

from agents import Runner, trace

from email_agent import email_agent
from planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from search_agent import search_agent
from writer_agent import Report, writer_agent


async def plan_searches(question: str) -> WebSearchPlan:
    result = await Runner.run(planner_agent, question)
    return result.final_output


async def search(item: WebSearchItem) -> str:
    result = await Runner.run(search_agent, f"Search term: {item.query}\nWhy: {item.reason}")
    return result.final_output


async def perform_searches(plan: WebSearchPlan) -> list[str]:
    return await asyncio.gather(*(search(item) for item in plan.searches))


async def write_report(question: str, results: list[str]) -> Report:
    summaries = "\n\n".join(results)
    result = await Runner.run(writer_agent, f"Question: {question}\n\nSearch summaries:\n{summaries}")
    return result.final_output


async def send_report(report: Report) -> None:
    steps = "\n".join(f"- {s}" for s in report.next_steps)
    await Runner.run(email_agent, f"{report.summary}\n\nNext steps:\n{steps}\n\n{report.report}")


async def run(question: str):
    start = time.time()
    with trace("Deep research"):
        yield "Planning the searches..."
        plan = await plan_searches(question)
        yield f"Searching the web for {len(plan.searches)} terms at once..."
        results = await perform_searches(plan)
        yield f"Writing the report from {len(results)} summaries..."
        report = await write_report(question, results)
        yield "Emailing the report..."
        await send_report(report)
    yield f"Done in {time.time() - start:.0f} s. Sent to the test inbox."
    yield report
