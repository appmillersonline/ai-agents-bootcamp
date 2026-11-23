import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from sidekick_tools import place_reorder

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[place_reorder],
    system_prompt="You help Sara reorder stock from her supplier.",
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"place_reorder": True})],
    checkpointer=InMemorySaver(),
)


async def ask(thread, text):
    config = {"configurable": {"thread_id": thread}}
    result = await agent.ainvoke({"messages": [("user", text)]}, config)
    request = result["__interrupt__"][0].value["action_requests"][0]
    print(f"Paused for Sara: {request['name']} {request['args']}")
    return config


async def decide(config, decision):
    result = await agent.ainvoke(Command(resume={"decisions": [decision]}), config)
    print("Agent:", result["messages"][-1].content, "\n")


async def main():
    print("--- 1. Approve ---")
    config = await ask("approve", "Reorder 12 Candle trios.")
    await decide(config, {"type": "approve"})

    print("--- 2. Edit ---")
    config = await ask("edit", "Reorder 12 Candle trios.")
    await decide(config, {"type": "edit", "edited_action": {"name": "place_reorder", "args": {"item": "Candle trio", "quantity": 6}}})

    print("--- 3. Reject ---")
    config = await ask("reject", "Reorder 40 Blue mug sets.")
    await decide(config, {"type": "reject", "message": "No: the supplier's mug kiln is closed until January."})


asyncio.run(main())
