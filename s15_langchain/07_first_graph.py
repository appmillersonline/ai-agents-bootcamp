import random
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

COLOURS = ["Fig", "Amber", "Sea Salt", "Cedar", "Lavender", "Honey"]
MOODS = ["Evening", "Morning", "Studio", "Harbour", "Winter", "Garden"]


class State(TypedDict):
    messages: Annotated[list, add_messages]


def name_candle(state: State) -> State:
    name = f"{random.choice(COLOURS)} {random.choice(MOODS)}"
    return {"messages": [("assistant", f"New candle name: {name}")]}


builder = StateGraph(State)
builder.add_node("name_candle", name_candle)
builder.add_edge(START, "name_candle")
builder.add_edge("name_candle", END)
graph = builder.compile()

graph.get_graph().print_ascii()
result = graph.invoke({"messages": [("user", "Name a candle")]})
print(result["messages"][-1].content)
