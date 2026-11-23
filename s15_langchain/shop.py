"""Shared helpers for the LangChain and LangGraph section: Sara's real stock list and the check_stock tool."""
import csv
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv(override=True)

DATA = Path(__file__).parents[1] / "data"


def load_stock() -> dict[str, dict]:
    with open(DATA / "inventory.csv") as f:
        return {row["item"].lower(): row for row in csv.DictReader(f)}


@tool
def check_stock(item: str) -> str:
    """Check how many of one product Sara has in stock, and whether it needs reordering."""
    row = load_stock().get(item.lower())
    if row is None:
        return f"'{item}' is not a product in Sara's shop."
    left, reorder_at = int(row["in_stock"]), int(row["reorder_at"])
    status = "needs reordering" if left <= reorder_at else "fine"
    return f"{row['item']}: {left} in stock (reorder at {reorder_at}), {status}."


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information. Use one short, specific query.
    Returns a short summary with the source links."""
    from openai import OpenAI

    response = OpenAI().responses.create(model="gpt-5.4-mini", tools=[{"type": "web_search"}], input=query)
    return response.output_text


def tools_used(result) -> list[str]:
    """The names of the tools an agent called, in order."""
    return [c["name"] for m in result["messages"] for c in getattr(m, "tool_calls", None) or []]
