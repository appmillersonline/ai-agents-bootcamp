"""Turn the week's changes into a short report, and send it to Sara's test inbox."""
import asyncio

from agents import Agent, Runner
from pydantic import BaseModel

from inbox import send_email
from settings import MODEL
from watch import watch


class Report(BaseModel):
    subject: str
    body: str


writer = Agent(
    name="Report writer",
    instructions="""You write Sara's Monday competitor report. Sara runs a small homeware shop with hand-poured candles.
Plain text email, no markdown symbols. Sections: Prices, New products, News, Market news, What you could do this week
(2 or 3 concrete ideas). Keep every number. Under 300 words. Sign it 'Your competitor watch'.""",
    model=MODEL,
    output_type=Report,
)


async def main():
    changes, news = await watch()
    found = "\n\n".join(c.model_dump_json(indent=1) for c in changes)
    result = await Runner.run(writer, f"Changes this week:\n{found}\n\nMarket news:\n{news}")
    report = result.final_output
    print(send_email("sara@example.com", report.subject, report.body))
    print("\n" + report.subject + "\n\n" + report.body)


asyncio.run(main())
