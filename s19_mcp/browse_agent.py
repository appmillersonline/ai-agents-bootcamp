"""A web-browsing agent built from two MCP servers: Playwright drives a real browser, Files saves the result."""
import asyncio
import sys
from collections import Counter
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, create_static_tool_filter
from dotenv import load_dotenv

load_dotenv(override=True)
SANDBOX = str(Path(__file__).parent / "sandbox")
BROWSER = {"command": "npx", "args": ["-y", "@playwright/mcp@latest", "--headless", "--isolated"]}
FILES = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", SANDBOX]}

INSTRUCTIONS = (f"You browse the web to complete tasks for Sara's shop. Only read pages; never fill in forms or buy anything. "
                f"When you save a file, save it inside {SANDBOX} only. "
                "If you can't read a value on the page, write 'unknown'. Never guess.")
TASK = ("On https://books.toscrape.com (a practice bookshop), open the Travel category. Take a snapshot of that page, "
        "read the price of every book on it, and pick the lowest. Then open that book's page. "
        "Save a note called book_pick.md with its title, price, star rating and page link, in at most 5 lines.")


READ_ONLY_BROWSER = ["browser_navigate", "browser_navigate_back", "browser_find", "browser_click",
                     "browser_snapshot", "browser_wait_for", "browser_close"]  # no forms, no uploads, no custom code


async def main():
    safe = "--safe" in sys.argv
    browser_tools = create_static_tool_filter(allowed_tool_names=READ_ONLY_BROWSER) if safe else None
    files_tools = create_static_tool_filter(allowed_tool_names=["write_file", "list_allowed_directories"])
    async with MCPServerStdio(params=BROWSER, name="browser", tool_filter=browser_tools, client_session_timeout_seconds=60) as browser, \
               MCPServerStdio(params=FILES, name="files", tool_filter=files_tools, client_session_timeout_seconds=60) as files:
        agent = Agent(name="shop_researcher", instructions=INSTRUCTIONS, model="gpt-5.4-mini", mcp_servers=[browser, files])
        result = await Runner.run(agent, TASK, max_turns=20)
    calls = [item.raw_item.name for item in result.new_items if item.type == "tool_call_item"]
    print("tool calls, in order:", " -> ".join(calls))
    print("totals:", dict(Counter(calls)))
    print("\n" + result.final_output)


asyncio.run(main())
