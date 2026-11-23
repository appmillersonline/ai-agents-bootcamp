"""Meeting-notes agent, step 2: put the meeting's tasks on the team's task board, and tell each owner on their phone."""
from meeting_notes import read_meeting
from task_board_lib import DATA, add_to_board, draw_board, load_board, notify

MEETING = "team_meeting_2026-11-02.txt"
if any(card["meeting"] == MEETING for card in load_board()):
    raise SystemExit("This meeting is already on the board.")  # AI wording changes each run, so check the meeting

notes = read_meeting(DATA / "meetings" / MEETING)
for task in notes.tasks:
    add_to_board(task, MEETING)
    print(f"added  {task.owner:<10} {task.title}")
for owner in ["Sara", "Leo", "Nadia"]:
    mine = [t.title for t in notes.tasks if t.owner == owner]
    if mine:
        notify(f"{owner}, new tasks from today's meeting: " + "; ".join(mine))
unowned = [t.title for t in notes.tasks if t.owner == "nobody yet"]
if unowned:
    notify("Sara, these tasks have no owner yet: " + "; ".join(unowned))
draw_board()
print("Board saved: data/task_board.html. Owners notified.")
