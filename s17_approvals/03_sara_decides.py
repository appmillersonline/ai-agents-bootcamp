import sys

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from approvals import make_graph

name, answer = sys.argv[1], sys.argv[2]  # e.g. vase approve

with SqliteSaver.from_conn_string("approvals.db") as memory:
    graph = make_graph(memory)
    config = {"configurable": {"thread_id": name}}
    waiting = graph.get_state(config)
    print("Waiting at:", waiting.next, "|", waiting.tasks[0].interrupts[0].value)
    result = graph.invoke(Command(resume=answer), config)
    print(f"Sara said {answer}: {result['decision']} (decided by {result['decided_by']})")
