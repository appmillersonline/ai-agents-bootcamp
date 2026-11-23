"""Sara's toolbox for the Sidekick: stock, web search, files, the browser, and two tools that need her approval."""
import csv
from contextlib import AsyncExitStack
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from openai import OpenAI

load_dotenv(override=True)

ROOT = Path(__file__).parents[1]
SANDBOX = Path(__file__).parent / "sandbox"
OUTBOX = ROOT / "outbox"
BROWSER = {"playwright": {"transport": "stdio", "command": "npx",
                          "args": ["-y", "@playwright/mcp@0.0.84", "--headless", "--isolated"]}}
BROWSER_TOOLS = {"browser_navigate", "browser_snapshot", "browser_click", "browser_navigate_back"}


@tool
def check_stock(item: str) -> str:
    """Check how many of one product Sara has in stock, and whether it needs reordering."""
    with open(ROOT / "data" / "inventory.csv") as f:
        rows = {r["item"].lower(): r for r in csv.DictReader(f)}
    row = rows.get(item.lower())
    if row is None:
        return f"'{item}' is not a product in Sara's shop."
    left, reorder_at = int(row["in_stock"]), int(row["reorder_at"])
    return f"{row['item']}: {left} in stock (reorder at {reorder_at}), {'needs reordering' if left <= reorder_at else 'fine'}."


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information. Use one short, specific query."""
    return OpenAI().responses.create(model="gpt-5.4-mini", tools=[{"type": "web_search"}], input=query).output_text


@tool
def write_file(filename: str, content: str) -> str:
    """Write a Markdown or text file in the Sidekick's sandbox folder."""
    (SANDBOX / Path(filename).name).write_text(content)
    return f"Wrote {filename}"


@tool
def read_file(filename: str) -> str:
    """Read a file from the Sidekick's sandbox folder."""
    return (SANDBOX / Path(filename).name).read_text()


@tool
def notify_sara(message: str) -> str:
    """Send Sara a short note. It lands in her outbox, which she checks on her phone."""
    with open(OUTBOX / "sidekick_notes.md", "a") as f:
        f.write(f"- {datetime.now():%Y-%m-%d %H:%M} {message}\n")
    return "Note sent to Sara."


@tool
def place_reorder(item: str, quantity: int) -> str:
    """Place a reorder with the supplier for one product."""
    with open(OUTBOX / "supplier_orders.md", "a") as f:
        f.write(f"- {datetime.now():%Y-%m-%d %H:%M} {quantity} x {item}\n")
    return f"Reorder placed: {quantity} x {item}."


class Browser:
    """Keeps one Playwright browser open for the whole Sidekick session (one MCP session, not one per call)."""

    async def start(self):
        self.stack = AsyncExitStack()
        client = MultiServerMCPClient(BROWSER)
        session = await self.stack.enter_async_context(client.session("playwright"))
        return [t for t in await load_mcp_tools(session) if t.name in BROWSER_TOOLS]

    async def close(self):
        await self.stack.aclose()
