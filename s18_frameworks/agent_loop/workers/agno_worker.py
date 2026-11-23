"""Agno worker."""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

from agent_loop.worker_tools import WORKER_PROMPT, make_tools

load_dotenv(override=True)
Agent(model=OpenAIChat(id="gpt-5.4-mini"), instructions=WORKER_PROMPT, tools=list(make_tools("agno"))).run("Do your task on the board.")
