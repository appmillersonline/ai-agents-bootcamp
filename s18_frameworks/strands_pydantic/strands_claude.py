"""Same Strands agent, different provider: one line changes the model to Claude."""
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel

from strands_pydantic.shop_data import stock_rows

model = LiteLLMModel(model_id="anthropic/claude-haiku-5-5")  # the only line that changed


@tool
def list_stock() -> list[dict]:
    """List every product in Sara's shop with how many are in stock and the reorder level."""
    return stock_rows()


agent = Agent(model=model, system_prompt="You help Sara run her small shop. Be brief.",
              tools=[list_stock], callback_handler=None)

result = agent("Which products are at or below their reorder level?")
print(result)
print("tools used:", list(result.metrics.tool_metrics))
