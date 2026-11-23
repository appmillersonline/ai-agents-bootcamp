from langchain_openai import ChatOpenAI

import shop  # noqa: F401  (loads the .env)

llm = ChatOpenAI(model="gpt-5.4-mini")
reply = llm.invoke("In one sentence, what makes a good product description for a small shop?")
print(reply.content)
