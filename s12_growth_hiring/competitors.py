"""Competitor watch agent: the competitors we watch, their pages, and the agent that spots what changed."""
from typing import Literal

from agents import Agent
from pydantic import BaseModel, Field

from settings import DATA, MODEL

COMPETITORS = {"Wick & Co": "wick_and_co", "Hearth Home": "hearth_home", "Lumen Studio": "lumen_studio"}


def page(competitor: str, week: str) -> str:
    return (DATA / "competitors" / COMPETITORS[competitor] / f"{week}.md").read_text()


class Change(BaseModel):
    kind: Literal["price", "launch", "news"]
    item: str = Field(description="The product or topic that changed.")
    before: str = Field(description="What it was last week, or 'nothing' if it is new.")
    after: str = Field(description="What it is this week.")
    why_it_matters: str = Field(description="One sentence on what this means for Sara's candle shop.")


class Changes(BaseModel):
    competitor: str
    changes: list[Change]


spotter = Agent(
    name="Change spotter",
    instructions="""You compare two snapshots of a competitor's shop page: last week and this week.
List every real change in prices, new products (launches) and news.
Ignore anything that stayed the same. If nothing changed, return an empty list.
Sara runs a small homeware shop that sells hand-poured candles, wholesale too.""",
    model=MODEL,
    output_type=Changes,
)
