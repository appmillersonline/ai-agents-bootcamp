from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import shop  # noqa: F401

llm = ChatOpenAI(model="gpt-5.4-mini")
messages = [
    SystemMessage("You answer customers of Sara's Shop in exactly eight words."),
    HumanMessage("Do you ship to Norway?"),
]
print(llm.invoke(messages).content)
