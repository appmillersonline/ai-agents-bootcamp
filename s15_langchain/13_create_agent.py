from langchain.agents import create_agent

from shop import check_stock

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[check_stock],
    system_prompt="You help Sara run her handmade homeware shop. Use your tool to check stock.",
)

agent.get_graph().print_ascii()
result = agent.invoke({"messages": [("user", "Which of these need reordering: Candle trio, Ceramic vase, Blue mug set?")]})
print("\n" + result["messages"][-1].content)
