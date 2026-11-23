"""Structured outputs: the agent fills in a Python object instead of writing free text."""
import asyncio
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, Runner

load_dotenv()


class Triage(BaseModel):
    category: Literal["where is my order", "damaged item", "return", "question", "other"]
    urgent: bool = Field(description="True if there's a deadline or the customer is very upset")
    order_id: str | None = Field(description="The order number, if the customer gave one")
    summary: str = Field(description="What the customer wants, in one short sentence")


triage_agent = Agent(
    name="Triage",
    instructions="You sort customer messages for Sara's shop.",
    model="gpt-5.4-mini",
    output_type=Triage,
)

MESSAGES = [
    "My candle set from order 1043 arrived with a cracked jar and it's a gift for tomorrow!",
    "Hi, do your mugs go in the dishwasher?",
    "I'd like to send back the tote bag from order 1041, it's the wrong colour.",
]


async def main():
    for message in MESSAGES:
        result = await Runner.run(triage_agent, message)
        triage = result.final_output
        flag = "URGENT " if triage.urgent else ""
        print(f"{flag}[{triage.category}] order {triage.order_id}: {triage.summary}")


asyncio.run(main())
