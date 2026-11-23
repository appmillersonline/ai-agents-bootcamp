from langgraph.checkpoint.sqlite import SqliteSaver

from graph_parts import make_builder

config = {"configurable": {"thread_id": "sara-reorders"}}

with SqliteSaver.from_conn_string("memory.db") as memory:
    graph = make_builder().compile(checkpointer=memory)

    now = graph.get_state(config)
    print("Messages in this thread now:", len(now.values["messages"]))

    history = list(graph.get_state_history(config))
    print("Saved checkpoints:", len(history))
    for snap in reversed(history):
        print(f"  step {snap.metadata['step']:>2}  next={snap.next}  messages={len(snap.values.get('messages', []))}")

    # Go back to the checkpoint right after Sara's first question was answered, and ask something else
    first_answer = next(s for s in reversed(history) if s.metadata["step"] >= 1 and not s.next)
    print("\nRewinding to step", first_answer.metadata["step"])
    replay = graph.invoke({"messages": [("user", "Actually, check the Blue mug set instead.")]}, first_answer.config)
    print("Bot (new branch):", replay["messages"][-1].content)
