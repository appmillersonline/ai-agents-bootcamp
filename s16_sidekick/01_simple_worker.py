import asyncio

from langchain.agents import create_agent

from sidekick_tools import check_stock, notify_sara, web_search

worker = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[check_stock, web_search, notify_sara],
    system_prompt="You are Sara's Sidekick, a helpful assistant for her handmade homeware shop. Use your tools to complete the task.",
)


async def main():
    task = "Check whether the Candle trio needs reordering, and send Sara a one-line note about it."
    result = await worker.ainvoke({"messages": [("user", task)]})
    print(result["messages"][-1].content)


asyncio.run(main())
