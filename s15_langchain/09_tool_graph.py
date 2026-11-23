from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from shop import check_stock

llm = ChatOpenAI(model="gpt-5.4-mini")
llm_with_tools = llm.bind_tools([check_stock])


class State(TypedDict):
    messages: Annotated[list, add_messages]
    customer_reply: str


def chatbot(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def write_reply(state: State) -> State:
    answer = state["messages"][-1].content
    prompt = f"Turn this stock answer into a two-sentence, friendly reply to a customer of Sara's Shop:\n{answer}"
    return {"customer_reply": llm.invoke(prompt).content}


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode([check_stock]))
builder.add_node("write_reply", write_reply)
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition, {"tools": "tools", END: "write_reply"})
builder.add_edge("tools", "chatbot")
builder.add_edge("write_reply", END)
graph = builder.compile()

graph.get_graph().print_ascii()
result = graph.invoke({"messages": [("user", "A customer asks: is the Candle trio in stock?")]})
print("\nSteps:", " -> ".join(m.type for m in result["messages"]))
print("Stock answer:  ", result["messages"][-1].content)
print("Customer reply:", result["customer_reply"])
