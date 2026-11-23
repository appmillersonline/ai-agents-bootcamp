from langchain_openai import ChatOpenAI

import shop  # noqa: F401

llm = ChatOpenAI(model="gpt-5.4-mini")
for chunk in llm.stream("Write a two-line welcome message for Sara's Shop, a handmade homeware shop."):
    print(chunk.content, end="", flush=True)
print()
