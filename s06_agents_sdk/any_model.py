"""Use any model with the SDK: the same agent code with Claude, and with a free model on your own computer."""
import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)  # traces go to OpenAI; we turn them off for the other providers

claude_client = AsyncOpenAI(base_url="https://api.anthropic.com/v1/", api_key=os.getenv("ANTHROPIC_API_KEY"))
ollama_client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

claude = OpenAIChatCompletionsModel(model="claude-haiku-5-5", openai_client=claude_client)
llama = OpenAIChatCompletionsModel(model="llama3.2:1b", openai_client=ollama_client)

INSTRUCTIONS = "You write one-sentence product descriptions for Sara's shop."


async def main():
    for model in ["gpt-5.4-mini", claude, llama]:
        agent = Agent(name="Writer", instructions=INSTRUCTIONS, model=model)
        result = await Runner.run(agent, "A handmade light-blue ceramic vase.")
        name = model if isinstance(model, str) else model.model
        print(f"{name}: {result.final_output}\n")


asyncio.run(main())
