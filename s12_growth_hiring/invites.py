"""Sara approves each invite, then the agent drafts it with real interview times and sends it."""
import asyncio

from agents import Agent, Runner, function_tool
from pydantic import BaseModel

from hiring_kit import MUST_HAVES, RESUMES, load, met, points
from inbox import send_email
from rank import assess_all
from settings import MODEL


@function_tool
def free_slots() -> str:
    """Sara's free interview times next week."""
    return "Tuesday 10 November at 10:00, Wednesday 11 November at 15:00, Friday 13 November at 11:00"


class Email(BaseModel):
    subject: str
    body: str


inviter = Agent(
    name="Invite writer",
    instructions="""Write a short, warm interview invitation from Sara, owner of a small homeware shop,
for the part-time candle maker and shop assistant job. Use your tool to offer her free times,
ask the candidate to reply with the one that suits them, and sign it as Sara. Plain text, under 120 words.""",
    model=MODEL,
    tools=[free_slots],
    output_type=Email,
)


async def main():
    ranked = await assess_all()
    shortlist = [(c, a) for c, a in ranked if MUST_HAVES <= met(a)][:3]
    for candidate, a in shortlist:
        print(f"\n{candidate}: {points(a)} points. {a.summary}")
        if input("Invite to an interview? (y/n) ").strip().lower() != "y":
            continue
        details, _ = load(next(p for p in RESUMES if p.stem == candidate))
        result = await Runner.run(inviter, f"Candidate's name: {details['Name']}")
        email = result.final_output
        print(send_email(details["Email"], email.subject, email.body))


asyncio.run(main())
