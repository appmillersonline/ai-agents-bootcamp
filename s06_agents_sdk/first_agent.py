"""Your first agent with the OpenAI Agents SDK: an Agent, the Runner, and a trace."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, trace

load_dotenv()

agent = Agent(
    name="Shop assistant",
    instructions="You help customers of Sara's shop, a small online shop for home goods. Be warm and short.",
    model="gpt-5.4-mini",
)


async def main():
    with trace("First agent"):
        result = await Runner.run(agent, "Suggest a gift under 30 euros for someone who loves tea.")
    print(result.final_output)
    print(result.to_input_list())  # every message in this run, as a list


asyncio.run(main())
