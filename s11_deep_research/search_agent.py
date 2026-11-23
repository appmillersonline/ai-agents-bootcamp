"""Agent 1: searches the web for one search term and sums up what it found."""
from agents import Agent, ModelSettings, WebSearchTool

from settings import MODEL

INSTRUCTIONS = """You research one search term for Sara, who runs a small homeware shop.
Search the web, then sum up what you found in under 200 words.
Keep real numbers, like prices and dates, and name the websites you used.
Write only the summary, in plain text: no markdown, no offers of more help."""

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    model=MODEL,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)
