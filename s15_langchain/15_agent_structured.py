from langchain.agents import create_agent
from pydantic import BaseModel, Field

from shop import check_stock


class ReorderList(BaseModel):
    reorder: list[str] = Field(description="Products that need reordering")
    fine: list[str] = Field(description="Products with enough stock")


agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[check_stock],
    system_prompt="You help Sara run her handmade homeware shop. Use your tool to check stock.",
    response_format=ReorderList,
)

result = agent.invoke({"messages": [("user", "Check the Candle trio, Linen tote bag, Ceramic vase and Blue mug set.")]})
report = result["structured_response"]
print(type(report).__name__)
print("reorder:", report.reorder)
print("fine:   ", report.fine)
