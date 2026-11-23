"""Agent 2: turns one big question into a few web searches."""
from pydantic import BaseModel, Field
from agents import Agent

from settings import HOW_MANY_SEARCHES, MODEL


class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search helps answer the question. Think about this first.")
    query: str = Field(description="The words to type into a search engine.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]


planner_agent = Agent(
    name="Planner",
    instructions=f"You plan web research for a small shop owner. "
                 f"Given a question, list {HOW_MANY_SEARCHES} different web searches that together answer it.",
    model=MODEL,
    output_type=WebSearchPlan,
)
