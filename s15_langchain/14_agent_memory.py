from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langgraph.checkpoint.memory import MemorySaver

from shop import check_stock


@wrap_tool_call
def log_tool_calls(request, handler):
    call = request.tool_call
    print(f"  [middleware] {call['name']}({call['args']})")
    return handler(request)


agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[check_stock],
    system_prompt="You help Sara run her handmade homeware shop. Use your tool to check stock.",
    checkpointer=MemorySaver(),
    middleware=[log_tool_calls],
)

config = {"configurable": {"thread_id": "monday-stock"}}
for text in ["I'm checking the Candle trio today.", "And how about the Linen tote bag? Which of the two is lower?"]:
    print("You:", text)
    result = agent.invoke({"messages": [("user", text)]}, config)
    print("Agent:", result["messages"][-1].content, "\n")
