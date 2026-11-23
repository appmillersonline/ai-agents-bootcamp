from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from shop import tools_used, web_search

SANDBOX = Path(__file__).parent / "sandbox"

market_researcher = {
    "name": "market-researcher",
    "description": "Researches one Christmas market and returns its dates, how to apply, and the stall cost.",
    "system_prompt": "You research one market with your search tool and return three short facts a small maker would care about, with a source link.",
    "tools": [web_search],
}

lead = create_deep_agent(
    model="openai:gpt-5.4-mini",
    system_prompt="You write short comparison briefings for Sara's Shop. Delegate the research on each market to a sub-agent.",
    subagents=[market_researcher],
    backend=FilesystemBackend(root_dir=SANDBOX, virtual_mode=True),
)

brief = (
    "Compare two Lisbon Christmas markets from markets.md as places for Sara to sell her candles and mugs. "
    "Research each one, then write a short comparison with a recommendation to compare.md."
)
result = lead.invoke({"messages": [("user", brief)]})
print("Tools used:", " -> ".join(tools_used(result)))
print("\n" + result["messages"][-1].text)
