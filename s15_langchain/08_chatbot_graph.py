from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

import shop  # noqa: F401

llm = ChatOpenAI(model="gpt-5.4-mini")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

result = graph.invoke({"messages": [("user", "In one sentence, what is a flowchart?")]})
for m in result["messages"]:
    print(f"{m.type:>6}: {m.content}")
