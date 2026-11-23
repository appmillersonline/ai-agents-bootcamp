"""Sara's stock check with Strands Agents (AWS)."""
from strands import Agent, tool
from strands.models.openai import OpenAIModel

from strands_pydantic.shop_data import stock_rows

model = OpenAIModel(model_id="gpt-5.4-mini")


@tool
def list_stock() -> list[dict]:
    """List every product in Sara's shop with how many are in stock and the reorder level."""
    return stock_rows()


agent = Agent(
    model=model,
    system_prompt="You help Sara run her small shop. Be brief.",
    tools=[list_stock],
    callback_handler=None,  # don't stream text as it arrives; we print the result at the end
)

result = agent("Which products are at or below their reorder level?")
print(result)
print("tools used:", list(result.metrics.tool_metrics))
