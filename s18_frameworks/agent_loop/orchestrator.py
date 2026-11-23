"""Project 8: an ADK orchestrator runs five workers, built with five frameworks, through one shared board."""
import asyncio
import logging
import subprocess
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from agent_loop import board, quality
from shop_helper.agent import MODEL

logging.getLogger("google_adk").setLevel(logging.ERROR)
HERE = Path(__file__).parents[1]
PY = sys.executable
WORKERS = {  # owner name on the board -> the command that starts that framework's worker
    "strands": [PY, "-m", "agent_loop.workers.strands_worker"],
    "pydantic_ai": [PY, "-m", "agent_loop.workers.pydantic_worker"],
    "maf": [PY, "-m", "agent_loop.workers.maf_worker"],
    "agno": [PY, "-m", "agent_loop.workers.agno_worker"],
    "mastra": ["npm", "run", "-s", "worker", "--prefix", str(HERE.parent / "s18_mastra")],
}


def add_task(owner: str, title: str, file: str) -> str:
    """Put one job on the shared board.

    Args:
        owner: One of: strands, pydantic_ai, maf, agno, mastra.
        title: What to write, in a few words.
        file: The Markdown file name to save, for example "product.md".
    """
    task_id = board.add_task(owner, title, file)
    print(f"  + #{task_id} {owner}: {title}", flush=True)
    return f"Added task #{task_id}."


def run_workers() -> str:
    """Start every worker that has an unfinished job, all at the same time, and wait for them."""
    owners = sorted({t["owner"] for t in board.tasks() if t["status"] != "done"})
    print(f"  > running in parallel: {', '.join(owners)}", flush=True)
    procs = [subprocess.Popen(WORKERS[o], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for o in owners]
    for p in procs:
        p.wait()
    print(board.show(), flush=True)
    return board.show()


def check_kit() -> str:
    """Score every finished file with the quality rules (name, price, at most one '!', word limit)."""
    lines, passed = [], 0
    for t in board.tasks():
        problems = quality.check(t)
        passed += not problems
        lines.append(f"#{t['id']} {t['file']}: " + ("OK" if not problems else "; ".join(problems)))
    print(f"  ? quality: {passed}/{len(lines)} pass", flush=True)
    for line in lines:
        if not line.endswith("OK"):
            print(f"    {line}", flush=True)
    return f"{passed}/{len(lines)} pass\n" + "\n".join(lines)


def redo_task(task_id: int, note: str) -> str:
    """Send one job back to its worker with a note saying what to fix.

    Args:
        task_id: The task number from the board.
        note: A short instruction, for example "remove extra exclamation marks".
    """
    board.set_status(task_id, "redo", note)
    print(f"  ! #{task_id} sent back: {note}", flush=True)
    return "Sent back."


orchestrator = Agent(
    name="orchestrator",
    model=MODEL,
    instruction=(
        "You run Sara's launch team. The product is the Lavender Candle Gift Box. "
        "1) Add one task per worker: strands writes the product page (product.md), pydantic_ai three FAQs (faq.md), "
        "maf the launch email (email.md), agno an Instagram post (instagram.md), mastra a shop counter card under 40 words (card.md). "
        "2) Call run_workers. 3) Call check_kit. 4) For every file that fails, call redo_task with a clear note, "
        "then run_workers and check_kit again. Stop when all pass or after two rounds of fixes. "
        "End with one short sentence for Sara."),
    tools=[add_task, run_workers, check_kit, redo_task],
)


async def main():
    board.reset()
    runner = InMemoryRunner(agent=orchestrator, app_name="launch")
    session = await runner.session_service.create_session(app_name="launch", user_id="sara")
    message = types.Content(role="user", parts=[types.Part(text="Build the launch kit for Friday.")])
    async for event in runner.run_async(user_id="sara", session_id=session.id, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"\norchestrator: {event.content.parts[0].text}")


asyncio.run(main())
