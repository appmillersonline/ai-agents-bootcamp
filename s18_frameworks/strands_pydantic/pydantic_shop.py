"""The same stock check with Pydantic AI, returning a typed restock plan."""
import os

os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")  # hide the start-up banner that suggests Logfire

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from strands_pydantic.shop_data import stock_rows


class Reorder(BaseModel):
    item: str
    in_stock: int
    order_qty: int = Field(description="How many to order to get back to twice the reorder level")


class RestockPlan(BaseModel):
    reorders: list[Reorder]
    note: str = Field(description="One short sentence for Sara")


def list_stock() -> list[dict]:
    """List every product in Sara's shop with how many are in stock and the reorder level."""
    return stock_rows()


agent = Agent(
    "openai:gpt-5.4-mini",
    instructions="You help Sara run her small shop. Reorder anything at or below its reorder level.",
    tools=[list_stock],
    output_type=RestockPlan,
)

result = agent.run_sync("Make this week's restock plan.")
plan = result.output  # a RestockPlan object, already checked by Pydantic
for r in plan.reorders:
    print(f"{r.item:<16} in stock {r.in_stock:>2}  ->  order {r.order_qty}")
print("Note:", plan.note)
print("tokens used:", result.usage.total_tokens)
