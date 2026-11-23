"""Way 2: a sales manager agent uses the three writers as tools and sends the best email itself."""
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, trace

from sales_kit import MODEL, WRITERS, send_email_tool

load_dotenv()

writer_tools = [w.as_tool(tool_name=w.name.lower().replace(" ", "_"),
                          tool_description="Writes one cold sales email. Tell it who the email is for.")
                for w in WRITERS]

manager = Agent(
    name="Sales manager",
    instructions="""You run Sara's small sales team.
1. Ask each of your three writers for one email draft.
2. Pick the draft a busy café owner would most likely answer.
3. Send only that one email with send_email_tool, then say which writer won and why.""",
    model=MODEL,
    tools=writer_tools + [send_email_tool],
)


async def main():
    with trace("Sales team: way 2"):
        result = await Runner.run(manager, "Pitch our wholesale candles to Lena at Café Lumen: lena@example.com")

    for item in result.new_items:
        if item.type == "tool_call_item":
            print("Manager called:", item.raw_item.name)
    print("\n" + result.final_output)


asyncio.run(main())
