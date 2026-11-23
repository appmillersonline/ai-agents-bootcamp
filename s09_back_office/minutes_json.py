"""The same minutes as JSON: the format other apps understand (task boards, calendars, spreadsheets)."""
from pathlib import Path

from meeting_notes import read_meeting

notes = read_meeting(Path(__file__).parent.parent / "data" / "meetings" / "team_meeting_2026-11-02.txt")
print(notes.model_dump_json(indent=2, include={"tasks"}))  # just the tasks, as JSON
print(f"\n{len(notes.decisions)} decisions, {len(notes.tasks)} tasks, "
      f"{sum(t.owner == 'nobody yet' for t in notes.tasks)} without an owner")
