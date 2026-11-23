from crewai.tools import tool
from openai import OpenAI


@tool("Search the web")
def web_search(query: str) -> str:
    """Search the web for up-to-date information. Use one short, specific query.
    Returns a short summary with the source links."""
    response = OpenAI().responses.create(model="gpt-5.4-mini", tools=[{"type": "web_search"}], input=query)
    return response.output_text
