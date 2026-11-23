"""Microsoft Agent Framework worker."""
import asyncio

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

from agent_loop.worker_tools import WORKER_PROMPT, make_tools

load_dotenv(override=True)
agent = Agent(client=OpenAIChatClient(model="gpt-5.4-mini"), name="maf", instructions=WORKER_PROMPT,
              tools=list(make_tools("maf")))
asyncio.run(agent.run("Do your task on the board."))
