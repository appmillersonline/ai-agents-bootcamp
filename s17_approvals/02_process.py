import json
import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from approvals import make_graph

requests = json.load(open("requests.json"))
names = sys.argv[1:] or ["mug", "tape", "candle", "vase"]

with SqliteSaver.from_conn_string("approvals.db") as memory:
    graph = make_graph(memory)
    for name in names:
        config = {"configurable": {"thread_id": name}}
        result = graph.invoke({"text": requests[name]}, config)
        f = result["form"]
        print(f"{name:7} {f['kind']:8} {f['amount_eur']:6.2f} EUR  -> {result['path']:9} {result['rule']}")
        if "__interrupt__" in result:
            print("        paused, waiting for Sara:", result["__interrupt__"][0].value["question"])
