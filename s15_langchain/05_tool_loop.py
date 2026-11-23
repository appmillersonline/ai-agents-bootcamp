from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from shop import check_stock

llm = ChatOpenAI(model="gpt-5.4-mini")
llm_with_tools = llm.bind_tools([check_stock])

messages = [HumanMessage("Do I need to reorder the Candle trio or the Linen tote bag?")]
reply = llm_with_tools.invoke(messages)
print("The model asks for:", [(c["name"], c["args"]) for c in reply.tool_calls])

messages.append(reply)
for call in reply.tool_calls:
    result = check_stock.invoke(call)
    print("We ran the tool:   ", result.content)
    messages.append(result)

final = llm_with_tools.invoke(messages)
print("\nFinal answer:", final.content)
