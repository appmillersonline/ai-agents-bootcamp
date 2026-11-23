"""Way 3: a reception agent reads a customer's reply and hands the job to the right specialist."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, trace

from sales_kit import MODEL, send_email_tool

load_dotenv()


@function_tool
def price_list() -> str:
    """Sara's wholesale prices and delivery terms."""
    return "24-71 candles: 9 euros each. 72 or more: 8 euros each. Free delivery over 300 euros, 5 working days."


@function_tool
def free_slots() -> str:
    """Times Sara is free for a call this week."""
    return "Tuesday 10:00, Wednesday 15:30, Friday 11:00"


prices = Agent(
    name="Prices",
    handoff_description="Questions about prices, discounts or delivery.",
    instructions="""Answer with the real numbers from price_list.
Send the reply with send_email_tool, signed Sara, then show the email you sent.""",
    model=MODEL,
    tools=[price_list, send_email_tool],
)

meetings = Agent(
    name="Meetings",
    handoff_description="The customer wants a call or a visit.",
    instructions="""Offer two times from free_slots.
Send the reply with send_email_tool, signed Sara, then show the email you sent.""",
    model=MODEL,
    tools=[free_slots, send_email_tool],
)

reception = Agent(
    name="Reception",
    instructions="You read replies to Sara's sales emails. Hand each one to the right colleague.",
    model=MODEL,
    handoffs=[prices, meetings],
)

REPLIES = [
    "From lena@example.com: Lovely idea! What would 80 candles cost, and how fast can you deliver?",
    "From tom@example.com: Interesting. Could we have a quick call this week? Tom, Hotel Azul",
]


async def main():
    for reply in REPLIES:
        with trace("Sales team: way 3"):
            result = await Runner.run(reception, reply)
        print(f"Handled by: {result.last_agent.name}\n{result.final_output}\n")


asyncio.run(main())
