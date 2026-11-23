"""Sara's shop helper, now with a teammate from ANOTHER company, reached over A2A."""
import asyncio
import logging

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from shop_helper.agent import MODEL, check_stock

logging.getLogger("google_adk").setLevel(logging.ERROR)

supplier = RemoteA2aAgent(
    name="cedar_and_wick",
    description="Sara's candle supplier: wholesale stock, prices and shipping times.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
)

shop_helper = Agent(
    name="shop_helper",
    model=MODEL,
    instruction=("You help Sara run her small home-goods shop. Use check_stock for her own stock. "
                 "If a candle is low or out of stock, ask cedar_and_wick about restocking."),
    tools=[check_stock],
    sub_agents=[supplier],
)


async def main():
    runner = InMemoryRunner(agent=shop_helper, app_name="shop")
    session = await runner.session_service.create_session(app_name="shop", user_id="sara")
    question = "We're out of the candle trio. Can we restock it this week?"
    print(f"Sara: {question}")
    message = types.Content(role="user", parts=[types.Part(text=question)])
    last = None
    async for event in runner.run_async(user_id="sara", session_id=session.id, new_message=message):
        for call in event.get_function_calls():
            print(f"   [{event.author}] calls {call.name}({dict(call.args)})")
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text != last:  # a remote agent can stream the same final answer twice
                print(f"{event.author}: {text}")
                last = text
    if last is None:  # the remote agent never answered (offline, wrong address, timeout)
        print("shop_helper: I couldn't reach Cedar & Wick right now. Please email them, or try again later.")


asyncio.run(main())
