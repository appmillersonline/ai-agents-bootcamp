"""Talk to Sara's shop helper from Python and watch every step: tool calls and hand-overs."""
import asyncio
import logging

from google.adk.runners import InMemoryRunner
from google.genai import types

from shop_helper.agent import root_agent

logging.getLogger("google_adk").setLevel(logging.ERROR)  # hide setup tips

QUESTIONS = [
    "Hi! Do you have the candle trio?",
    "Okay. And where is my order 1042?",
    "Thanks! Is the linen tote bag in stock too?",
]


async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="shop")
    session = await runner.session_service.create_session(app_name="shop", user_id="maya")
    for question in QUESTIONS:
        print(f"\nCustomer: {question}")
        message = types.Content(role="user", parts=[types.Part(text=question)])
        async for event in runner.run_async(user_id="maya", session_id=session.id, new_message=message):
            for call in event.get_function_calls():
                print(f"   [{event.author}] calls {call.name}({dict(call.args)})")
            if event.is_final_response() and event.content and event.content.parts:
                print(f"{event.author}: {event.content.parts[0].text}")


asyncio.run(main())
