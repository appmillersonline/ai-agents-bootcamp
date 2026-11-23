"""Pydantic AI worker: plain functions as tools."""
import os

os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")
from dotenv import load_dotenv
from pydantic_ai import Agent

from agent_loop.worker_tools import WORKER_PROMPT, make_tools

load_dotenv(override=True)
Agent("openai:gpt-5.4-mini", instructions=WORKER_PROMPT, tools=list(make_tools("pydantic_ai"))).run_sync("Do your task on the board.")
