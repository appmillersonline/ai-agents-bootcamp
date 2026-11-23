"""Meeting-notes agent, step 1: turn messy meeting notes into a summary, decisions and tasks with owners."""
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
import anthropic
from pydantic import BaseModel

load_dotenv()
client = anthropic.Anthropic()


class Task(BaseModel):
    title: str
    owner: Literal["Sara", "Leo", "Nadia", "nobody yet"]
    due: str | None  # YYYY-MM-DD
    priority: Literal["high", "normal"]


class MeetingNotes(BaseModel):
    summary: str
    decisions: list[str]
    tasks: list[Task]


def read_meeting(path: Path):
    response = client.messages.parse(
        model="claude-sonnet-5-5",  # notes are messy: the everyday all-rounder reads between the lines
        max_tokens=4000,
        system="You turn meeting notes for Sara's shop into clear minutes. The meeting was on 2 November 2026. "
               "Only include what the notes say. If nobody took a task, the owner is 'nobody yet'. "
               "Priority is high when it is due within two weeks or involves money. Write dates as YYYY-MM-DD.",
        messages=[{"role": "user", "content": path.read_text()}],
        output_format=MeetingNotes,
    )
    return response.parsed_output


if __name__ == "__main__":
    notes = read_meeting(Path(sys.argv[1]))
    print("SUMMARY:", notes.summary, "\n\nDECISIONS:")
    for d in notes.decisions:
        print(" -", d)
    print("\nTASKS:")
    for t in notes.tasks:
        print(f" - [{t.priority:<6}] {t.owner:<10} {t.due or 'no date':<11} {t.title}")
