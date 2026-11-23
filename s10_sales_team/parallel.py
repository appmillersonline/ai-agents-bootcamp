"""Way 1: our code runs the three writers at the same time, a picker chooses, and our code sends."""
import asyncio
import time
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, Runner, trace

from sales_kit import MODEL, WRITERS, send_email

load_dotenv()
TASK = "Write to Lena, owner of Café Lumen, a busy coffee shop."


class Pick(BaseModel):
    winner: Literal[1, 2, 3]
    reason: str


picker = Agent(
    name="Picker",
    instructions="You own a busy café. Pick the cold email you'd most likely answer, and say why in one sentence.",
    model=MODEL,
    output_type=Pick,
)


async def main():
    with trace("Sales team: way 1"):
        start = time.time()
        results = await asyncio.gather(*(Runner.run(w, TASK) for w in WRITERS))
        print(f"Three drafts in {time.time() - start:.1f} s\n")

        drafts = [r.final_output for r in results]
        options = "\n\n".join(f"Email {i}: {d.subject}\n{d.body}" for i, d in enumerate(drafts, 1))
        pick = (await Runner.run(picker, options)).final_output
        print(f"Picker chose email {pick.winner} ({WRITERS[pick.winner - 1].name}): {pick.reason}\n")

    best = drafts[pick.winner - 1]
    print(send_email("lena@example.com", best.subject, best.body))


asyncio.run(main())
