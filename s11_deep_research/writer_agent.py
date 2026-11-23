"""Agent 3: writes one clear report from all the search summaries."""
from pydantic import BaseModel, Field
from agents import Agent

from settings import MODEL

INSTRUCTIONS = """You write research reports for Sara, who runs a small homeware shop.
You get her question and summaries of several web searches.
Use only facts from the summaries. If sources disagree, say so. Keep the numbers."""


class Report(BaseModel):
    summary: str = Field(description="Two or three sentences that answer the question, for a busy owner.")
    report: str = Field(description="The full report in markdown, 400 to 700 words, with headings.")
    next_steps: list[str] = Field(description="Three practical things Sara could do next.")


writer_agent = Agent(name="Writer", instructions=INSTRUCTIONS, model=MODEL, output_type=Report)
