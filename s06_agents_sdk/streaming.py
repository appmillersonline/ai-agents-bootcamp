"""Streaming: print the answer word by word while it's being written, like ChatGPT does."""
import asyncio

from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

load_dotenv()

agent = Agent(name="Story writer", instructions="You write short product stories for Sara's shop.", model="gpt-5.4-mini")


async def main():
    result = Runner.run_streamed(agent, "Write a 4-sentence story about a handmade blue vase.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    print()


asyncio.run(main())
