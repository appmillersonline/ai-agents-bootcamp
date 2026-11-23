"""Recruiting assistant: the job, the resumes, and the agent that checks a resume against each requirement."""
import re

from agents import Agent
from pydantic import BaseModel, Field

from settings import DATA, MODEL

JOB = (DATA / "hiring" / "job.md").read_text()
RESUMES = sorted((DATA / "hiring" / "resumes").glob("*.txt"))
MUST_HAVES = {1, 2, 3, 4}


def load(path) -> tuple[dict, str]:
    """Split a resume into personal details (kept by our code) and the work history (all the agent sees)."""
    head, body = path.read_text().split("---\n", 1)
    details = dict(line.split(": ", 1) for line in head.strip().splitlines())
    return details, body.strip()


class Check(BaseModel):
    requirement: int = Field(description="The requirement number from the job description, 1 to 6.")
    evidence: str = Field(description="A short quote from the resume that proves it, or 'none'.")
    met: bool


class Assessment(BaseModel):
    checks: list[Check] = Field(description="One check for every requirement, 1 to 6.")
    summary: str = Field(description="Two sentences on strengths and missing requirements, based only on the resume.")


scorer = Agent(
    name="Resume scorer",
    instructions=f"""You check one resume against this job.

{JOB}
For every requirement, quote the evidence from the resume first, then decide if it is met.
Judge only skills, experience and availability. Never guess or mention age, gender, nationality, health or family,
and never count a break in work history against anyone.""",
    model=MODEL,
    output_type=Assessment,
)


def met(a: Assessment) -> set[int]:
    return {c.requirement for c in a.checks if c.met}


def points(a: Assessment) -> int:
    """Our code does the maths: 20 points per must-have, 10 per nice-to-have, so 100 is the top."""
    return sum(20 if r in MUST_HAVES else 10 for r in met(a))


BANNED = ["age", "young", "old", "older", "gender", "male", "female", "woman", "man", "pregnant", "married",
          "nationality", "religion", "native", "gap"]


def fairness_problems(a: Assessment) -> list[str]:
    """A plain-code guardrail: words that must never appear in a reason for a hiring score."""
    text = (a.summary + " " + " ".join(c.evidence for c in a.checks)).lower()
    return [word for word in BANNED if re.search(rf"\b{word}\b", text)]
