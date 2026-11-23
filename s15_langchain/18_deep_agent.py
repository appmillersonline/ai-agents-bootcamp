from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from shop import tools_used, web_search

SANDBOX = Path(__file__).parent / "sandbox"

agent = create_deep_agent(
    model="openai:gpt-5.4-mini",
    tools=[web_search],
    system_prompt=(
        "You are a research assistant for Sara's Shop, a small handmade homeware shop. "
        "Plan your work with your to-do tool, research with the search tool, "
        "and write your findings as a short Markdown briefing to a file."
    ),
    backend=FilesystemBackend(root_dir=SANDBOX, virtual_mode=True),
)

brief = (
    "Sara wants to sell at a Christmas market in Lisbon this December. "
    "Find two markets that take small makers, with their dates and how to apply. "
    "Write a one-page briefing to markets.md."
)
result = agent.invoke({"messages": [("user", brief)]})
print("Tools used:", " -> ".join(tools_used(result)))
print("\n" + result["messages"][-1].text)
