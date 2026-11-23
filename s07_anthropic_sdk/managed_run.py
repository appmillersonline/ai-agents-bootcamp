"""Managed Agents, step 2 (every run): start a session, give it a file and a job, watch it work."""
import json
import time
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
DATA = Path(__file__).parent.parent / "data"
ids = json.loads((DATA / "managed_ids.json").read_text())

sales = client.files.upload(file=DATA / "october_sales.csv")
session = client.beta.sessions.create(  # a fresh workspace, run by Anthropic
    agent={"type": "agent", "id": ids["agent"], "version": ids["version"]},
    environment_id=ids["environment"],
    resources=[{"type": "file", "file_id": sales.id, "mount_path": "/data/sales.csv"}],
)
JOB = ("Read /mnt/session/uploads/data/sales.csv. Write /mnt/session/outputs/report.md with the top 3 items by revenue "
       "(qty × price_eur) and revenue per weekday, best first. Then reply in one sentence.")

with client.beta.sessions.events.stream(session_id=session.id) as stream:
    client.beta.sessions.events.send(session_id=session.id,
                                     events=[{"type": "user.message", "content": [{"type": "text", "text": JOB}]}])
    for event in stream:
        if event.type == "agent.tool_use":
            print("Agent uses:", event.name)
            if event.evaluated_permission == "ask":  # nobody is watching, so say no
                client.beta.sessions.events.send(session_id=session.id, events=[
                    {"type": "user.tool_confirmation", "tool_use_id": event.id, "result": "deny"}])
        elif event.type == "agent.message":
            print("Agent:", "".join(b.text for b in event.content if b.type == "text"))
        elif event.type == "session.status_idle" and event.stop_reason.type != "requires_action":
            break
        elif event.type == "session.status_terminated":
            break

for attempt in range(15):  # output files take a few seconds to appear
    outputs = [f for f in client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"]).data
               if f.downloadable]  # skip the sales file we uploaded
    if outputs:
        break
    time.sleep(2)
for f in outputs:
    client.beta.files.download(f.id).write_to_file(DATA / f"managed_{f.filename}")  # copy the outputs home
    print("Saved:", f"data/managed_{f.filename}")
