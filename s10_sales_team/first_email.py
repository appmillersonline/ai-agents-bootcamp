"""One writer agent with the email tool writes to one café and sends it."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, trace

from sales_kit import MODEL, OFFER, send_email_tool

load_dotenv()

writer = Agent(
    name="Writer",
    instructions=OFFER + "\nSend the email with your tool, then say who it went to and the subject.",
    model=MODEL,
    tools=[send_email_tool],
)


async def main():
    with trace("First sales email"):
        result = await Runner.run(writer, "Write to Lena, owner of Café Lumen: lena@example.com")
    print(result.final_output)


asyncio.run(main())
