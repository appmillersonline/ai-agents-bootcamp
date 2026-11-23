from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

import shop  # noqa: F401


class ProductIdea(BaseModel):
    name: str = Field(description="A short product name")
    price_eur: int = Field(description="A sensible price in euros")
    tagline: str = Field(description="One calm sentence in Sara's voice")


llm = ChatOpenAI(model="gpt-5.4-mini")
structured_llm = llm.with_structured_output(ProductIdea)
idea = structured_llm.invoke("Suggest one new winter product for a handmade homeware shop.")
print(type(idea).__name__)
print(idea)
print("Price:", idea.price_eur, "euros")
