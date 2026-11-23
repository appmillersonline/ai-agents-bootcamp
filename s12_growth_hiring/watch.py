"""Watch every competitor at once, plus this week's market news from the web."""
import asyncio

from agents import Agent, ModelSettings, Runner, WebSearchTool, trace

from competitors import COMPETITORS, Changes, page, spotter
from settings import MODEL

news_agent = Agent(
    name="Market news",
    instructions="""Search the web for this week's news about the scented candle market in Europe:
trends, prices and big launches. Sum up the 3 most useful items for a small candle shop in under 120 words,
in plain text, and name the websites you used.""",
    model=MODEL,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)


async def spot(name: str) -> Changes:
    prompt = f"Competitor: {name}\n\nLAST WEEK:\n{page(name, 'last_week')}\n\nTHIS WEEK:\n{page(name, 'this_week')}"
    result = await Runner.run(spotter, prompt)
    return result.final_output


async def market_news() -> str:
    result = await Runner.run(news_agent, "What happened in the scented candle market this week?")
    return result.final_output


async def watch() -> tuple[list[Changes], str]:
    with trace("Competitor watch"):
        *changes, news = await asyncio.gather(*(spot(name) for name in COMPETITORS), market_news())
    return changes, news


if __name__ == "__main__":
    changes, news = asyncio.run(watch())
    for c in changes:
        print(f"\n{c.competitor}: {len(c.changes)} changes")
        for change in c.changes:
            print(f"  [{change.kind}] {change.item}: {change.before} -> {change.after}")
    print("\nMarket news:\n" + news)
