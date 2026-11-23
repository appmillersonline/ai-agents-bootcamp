from langgraph.checkpoint.memory import MemorySaver

from graph_parts import make_builder


def ask(graph, text, config=None):
    result = graph.invoke({"messages": [("user", text)]}, config)
    print(f"You: {text}\nBot: {result['messages'][-1].content}\n")


print("--- Without memory ---")
graph = make_builder().compile()
ask(graph, "Hi, I'm Sara. I'm checking the Ceramic vase today.")
ask(graph, "What's my name, and which product am I checking?")

print("--- With a MemorySaver checkpointer ---")
graph = make_builder().compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "sara-monday"}}
ask(graph, "Hi, I'm Sara. I'm checking the Ceramic vase today.", config)
ask(graph, "What's my name, and how many of that product do I have?", config)
