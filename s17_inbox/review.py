"""Sara's coffee review: every draft from this morning's run, waiting for her OK."""
from datetime import date

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from drafts import make_drafter

with SqliteSaver.from_conn_string("drafts.db") as memory:
    drafter = make_drafter(memory)
    threads = sorted({c.config["configurable"]["thread_id"] for c in memory.list(None)})
    for thread in [t for t in threads if t.startswith(str(date.today()))]:
        config = {"configurable": {"thread_id": thread}}
        state = drafter.get_state(config)
        if not state.next:
            continue
        draft = state.tasks[0].interrupts[0].value["action_requests"][0]["args"]
        print(f"\n=== To {draft['to']}: {draft['subject']}\n{draft['body']}\n")
        ok = input("Send it? (y/n): ").strip().lower().startswith("y")
        decision = {"type": "approve"} if ok else {"type": "reject", "message": "Sara will answer this one herself."}
        drafter.invoke(Command(resume={"decisions": [decision]}), config)
        print("->", "Sent." if ok else "Not sent.")
