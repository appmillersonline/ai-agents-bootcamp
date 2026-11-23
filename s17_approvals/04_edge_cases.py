import json

from langgraph.checkpoint.sqlite import SqliteSaver

from approvals import make_graph

requests = json.load(open("requests.json"))
with SqliteSaver.from_conn_string("approvals.db") as memory:
    graph = make_graph(memory)
    for name in ["late", "twenty", "pushy"]:
        result = graph.invoke({"text": requests[name]}, {"configurable": {"thread_id": name}})
        f = result["form"]
        print(f"{name:7} {f['amount_eur']:6.2f} EUR  photo={f['has_photo']!s:5}  -> {result['path']:9} {result['rule']}")
