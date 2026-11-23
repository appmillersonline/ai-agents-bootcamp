import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from graph_parts import make_builder

config = {"configurable": {"thread_id": "sara-reorders"}}
text = " ".join(sys.argv[1:])

with SqliteSaver.from_conn_string("memory.db") as memory:
    graph = make_builder().compile(checkpointer=memory)
    result = graph.invoke({"messages": [("user", text)]}, config)
    print("Bot:", result["messages"][-1].content)
