"""The same output check without the SDK's guardrail feature: two runs and an if statement."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner

from guardrails import SHOP, output_checker

load_dotenv()

writer = Agent(name="Support", model="gpt-5.4-mini", instructions=SHOP)


async def main():
    draft = (await Runner.run(writer, "My vase arrived broken. Can you just refund me right now?")).final_output
    check = (await Runner.run(output_checker, draft)).final_output
    if check.problem:
        print("Not sent:", check.reason)
    else:
        print("Sent:", draft)


asyncio.run(main())
