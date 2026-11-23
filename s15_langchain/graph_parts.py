"""The stock-check graph from 09_tool_graph.py as a builder, so later scripts can compile it with memory."""
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from shop import check_stock

llm_with_tools = ChatOpenAI(model="gpt-5.4-mini").bind_tools([check_stock])


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def make_builder() -> StateGraph:
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode([check_stock]))
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    return builder
